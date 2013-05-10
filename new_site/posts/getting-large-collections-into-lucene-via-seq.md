<!-- 
.. link: 
.. description: a passionate tale of a daring rescue from a burning house 
.. tags: clueweb,hadoop,lucene
.. date: Fri Apr 08 10:15:23 -0700 2011
.. title: Getting large collections into Lucene via SequenceFiles
.. slug: getting-large-collections-into-lucene-via-seq
-->
I had a problem while setting up my indexing job for the ClueWeb09 collection. I wanted to do it from a MapReduce job: take each document, break it down into indexable chunks (title, URL, metadata, text, anchors) keyed by URL, sort around to accumulate the anchors for each document, then dump to an IndexWriter writing to local storage in the reduce phase.

Great idea, only Lucene would get into long periods of juggling files in the FSDirectory, and the reduce jobs would time out. My cluster would run 36 reduce jobs, and each one at the end (using the different process I'm about to describe) produced a 55GB index of around 14 million documents. Maybe this was expected, maybe not.

So here's what I did instead: the indexable chunks are sorted down in the reduce phase and written out to LZO-compressed SequenceFiles. Here's how it works... this code is too closely tied up in our larger IR system to easily post the code up to a repository, so you'll have to make do with snippets and pseudocode this time around.

The Mapper job takes each document, parses out the headers, text, anchors, bacon, and coffee, and puts each one into what I call a ParseTuple. A ParseTuple is a (key, value) pair. Note that this is a simple WritableComparable.

    import java.io.IOException;
    import java.io.DataInput;
    import java.io.DataOutput;

    import org.apache.hadoop.io.Text;
    import org.apache.hadoop.io.WritableComparable;

    public class ParseTuple implements WritableComparable&lt;ParseTuple&gt; {
        protected String label;
        protected String data;

        public ParseTuple() {
            label = null;
            data = null;
        }
        public ParseTuple(String a, String b) {
            label = a;
            data = b;
        }
        public void write(DataOutput out) throws IOException {
            Text.writeString(out, label);
            Text.writeString(out, data);
        }
        public void readFields(DataInput in) throws IOException {
            label = Text.readString(in);
            data = Text.readString(in);
        }
        public static ParseTuple read(DataInput in) throws IOException {
            ParseTuple pt = new ParseTuple();
            pt.readFields(in);
            return pt;
        }
        public int compareTo(ParseTuple other) {
            if (label.equals("ptext"))
                return -1;
            else if (other.label.equals("ptext"))
                return 1;
            else
                return label.compareTo(other.label);
        }
        public String toString() {
            return new String(label + ":" + data);
        }
    }

The Mapper class as you know emits (key, value) pairs.  In this case, the mapper maps documents to (URL, ParseTuple) pairs.  The keys inside each ParseTuple are used to identify how I want each tuple indexed - what Lucene Field, essentially, the data should go into.

The Reducer is going to compile all the ParseTuples for a given URL into what I call a DocBits.  Again, it's a simple serializable Map, so that the reducer can emit a single value for each URL.  Here's DocBits:

    import java.io.IOException;
    import java.io.DataInput;
    import java.io.DataOutput;
    import java.util.HashMap;
    import java.util.Map;

    import org.apache.hadoop.io.Text;
    import org.apache.hadoop.io.Writable;
    import org.apache.hadoop.mapreduce.Reducer;

    public class DocBits implements Writable {
        protected HashMap&lt;String, String&gt; map;

        public DocBits() {
            map = new HashMap();
        }
        public void add(String k, String v) {
            map.put(k, v);
        }
        public void add(ParseTuple p) {
            map.put(p.label, p.data);
        }
        public void write(DataOutput out) throws IOException {
            for (Map.Entry&lt;String, String&gt; e : map.entrySet()) {
                Text.writeString(out, e.getKey());
                Text.writeString(out, e.getValue());
            }
            Text.writeString(out, "EOD");
        }

        public void readFields(DataInput in) throws IOException {
            while (true) {
                String k = Text.readString(in);
                if (k.equals("EOD"))
                    break;
                String v = Text.readString(in);
                map.put(k, v);
            }
        }

        public static DocBits read(DataInput in) throws IOException {
            DocBits db = new DocBits();
            db.readFields(in);
            return db;
        }
    }

The Reducer is very simple:

    import java.io.IOException;
    import java.util.Map;
    import java.util.HashMap;
    import java.util.regex.Pattern;
             
    import org.apache.hadoop.io.Text;
    import org.apache.hadoop.mapreduce.Reducer;

    public class ReduceParseTuplesToDocBits
        extends Reducer&lt;Text, ParseTuple, Text, DocBits&gt; {
        
        public void reduce(Text key, Iterable&lt;ParseTuple&gt; values, 
                           Context context)
            throws IOException, InterruptedException {
            
            DocBits doc = new DocBits();
            StringBuilder anchors = new StringBuilder(65536);
            StringBuilder title = new StringBuilder(8096);
            boolean have_parsed_doc = false;

            doc.add("url", key.toString());
            context.setStatus(key.toString());

            for (ParseTuple t: values) {
                if (t.label.equals("ptext")) {
                    doc.add("ptext", t.data);
                    have_parsed_doc = true;
                } else if (t.label.equals("title"))
                    title.append(t.data).append(" ");
                else if (t.label.equals("anchor") &amp;&amp; anchors.length() &lt; 65536)
                    anchors.append(t.data).append(" ");

                else
                    doc.add(t);

                context.progress();
            }

            if (have_parsed_doc) {
                if (anchors.length() &gt; 0)
                    doc.add("anchor", anchors.toString());
                if (title.length() &gt; 0)
                    doc.add("title", title.toString());

                context.write(key, doc);
            }
        }
    }

The reducer has to be a little clever, because the Mapper will emit anchortext for documents that aren't in the collection.  We could actually index that if we wanted to, but we don't, since our job is only to search within the collection.

The main class that runs the job sets up the Mapper, Reducer, and the compressed SequenceFile:


       public int run(String[] args) throws Exception {
            Configuration conf = getConf();

            Job job = new Job(conf, "p3l.MapReduceIndexer");
             
            job.setJarByClass(this.getClass());
            LOG.info("Jar is " + job.getJar());

            job.setMapperClass(MapWebDocToParseTuple.class);
            job.setMapOutputKeyClass(Text.class);
            job.setMapOutputValueClass(ParseTuple.class);

            job.setReducerClass(ReduceParseTuplesToDocBits.class);
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(DocBits.class);

            job.setInputFormatClass(ClueWebInputFormat.class); // default
            job.setOutputFormatClass(SequenceFileOutputFormat.class);

            FileInputFormat.setInputPaths(job, new Path(args[1]));
            SequenceFileOutputFormat.setOutputPath(job, new Path(args[2]));
            SequenceFileOutputFormat.setCompressOutput(job, true);
            SequenceFileOutputFormat.setOutputCompressorClass(job, com.hadoop.compression.lzo.LzoCodec.class);
            SequenceFileOutputFormat.setOutputCompressionType(job, SequenceFile.CompressionType.BLOCK);
             
            // job.submit();
            return (job.waitForCompletion(true) ? 0 : 1);
        }

So at the end of this job, each Reducer has created a 26GB LZO-compressed SequenceFile ready to index:    

    [soboroff@node1 ~]$ hadoop fs -ls clue
    Found 38 items
    -rw-r--r--   3 soboroff hadoop           0 2011-02-08 14:09 /user/soboroff/clue/_SUCCESS
    drwxrwxr-x   - soboroff hadoop           0 2011-02-07 15:38 /user/soboroff/clue/_logs
    -rw-r--r--   3 soboroff hadoop 26327668533 2011-02-08 08:18 /user/soboroff/clue/part-r-00000
    -rw-r--r--   3 soboroff hadoop 26339468375 2011-02-08 08:18 /user/soboroff/clue/part-r-00001
    -rw-r--r--   3 soboroff hadoop 26330501868 2011-02-08 08:17 /user/soboroff/clue/part-r-00002
    -rw-r--r--   3 soboroff hadoop 26366091781 2011-02-08 08:14 /user/soboroff/clue/part-r-00003
    -rw-r--r--   3 soboroff hadoop 26321214072 2011-02-08 08:16 /user/soboroff/clue/part-r-00004
    -rw-r--r--   3 soboroff hadoop 26349081494 2011-02-08 08:18 /user/soboroff/clue/part-r-00005
    -rw-r--r--   3 soboroff hadoop 26343308176 2011-02-08 08:28 /user/soboroff/clue/part-r-00006
    -rw-r--r--   3 soboroff hadoop 26352600382 2011-02-08 08:24 /user/soboroff/clue/part-r-00007
    -rw-r--r--   3 soboroff hadoop 26321726649 2011-02-08 08:18 /user/soboroff/clue/part-r-00008
    -rw-r--r--   3 soboroff hadoop 26339094476 2011-02-08 08:10 /user/soboroff/clue/part-r-00009
    -rw-r--r--   3 soboroff hadoop 26321564045 2011-02-08 08:16 /user/soboroff/clue/part-r-00010
    -rw-r--r--   3 soboroff hadoop 26343854112 2011-02-08 08:10 /user/soboroff/clue/part-r-00011
    -rw-r--r--   3 soboroff hadoop 26315754762 2011-02-08 08:15 /user/soboroff/clue/part-r-00012
    -rw-r--r--   3 soboroff hadoop 26346819081 2011-02-08 08:18 /user/soboroff/clue/part-r-00013
    -rw-r--r--   3 soboroff hadoop 26364417290 2011-02-08 08:10 /user/soboroff/clue/part-r-00014
    -rw-r--r--   3 soboroff hadoop 26345720864 2011-02-08 08:15 /user/soboroff/clue/part-r-00015
    -rw-r--r--   3 soboroff hadoop 26325886676 2011-02-08 08:19 /user/soboroff/clue/part-r-00016
    -rw-r--r--   3 soboroff hadoop 26352366823 2011-02-08 08:16 /user/soboroff/clue/part-r-00017
    -rw-r--r--   3 soboroff hadoop 26363877289 2011-02-08 08:10 /user/soboroff/clue/part-r-00018
    -rw-r--r--   3 soboroff hadoop 26346838673 2011-02-08 08:23 /user/soboroff/clue/part-r-00019
    -rw-r--r--   3 soboroff hadoop 26334634232 2011-02-08 08:18 /user/soboroff/clue/part-r-00020
    -rw-r--r--   3 soboroff hadoop 26338242486 2011-02-08 08:15 /user/soboroff/clue/part-r-00021
    -rw-r--r--   3 soboroff hadoop 26333691832 2011-02-08 08:11 /user/soboroff/clue/part-r-00022
    -rw-r--r--   3 soboroff hadoop 26351824723 2011-02-08 08:13 /user/soboroff/clue/part-r-00023
    -rw-r--r--   3 soboroff hadoop 26340649075 2011-02-08 08:14 /user/soboroff/clue/part-r-00024
    -rw-r--r--   3 soboroff hadoop 26348830107 2011-02-08 08:11 /user/soboroff/clue/part-r-00025
    -rw-r--r--   3 soboroff hadoop 26341221269 2011-02-08 08:17 /user/soboroff/clue/part-r-00026
    -rw-r--r--   3 soboroff hadoop 26318480301 2011-02-08 08:09 /user/soboroff/clue/part-r-00027
    -rw-r--r--   3 soboroff hadoop 26314900021 2011-02-08 08:22 /user/soboroff/clue/part-r-00028
    -rw-r--r--   3 soboroff hadoop 26335481459 2011-02-08 08:16 /user/soboroff/clue/part-r-00029
    -rw-r--r--   3 soboroff hadoop 26329189695 2011-02-08 08:22 /user/soboroff/clue/part-r-00030
    -rw-r--r--   3 soboroff hadoop 26347416304 2011-02-08 08:14 /user/soboroff/clue/part-r-00031
    -rw-r--r--   3 soboroff hadoop 26340982688 2011-02-08 08:27 /user/soboroff/clue/part-r-00032
    -rw-r--r--   3 soboroff hadoop 26327061702 2011-02-08 08:18 /user/soboroff/clue/part-r-00033
    -rw-r--r--   3 soboroff hadoop 26331125728 2011-02-08 08:12 /user/soboroff/clue/part-r-00034
    -rw-r--r--   3 soboroff hadoop 26328859269 2011-02-08 08:09 /user/soboroff/clue/part-r-00035

And lastly, I have a stand-alone application which uses a SequenceFile.Reader to read each DocBits and build it into a Lucene Document, which gets passed on to an IndexWriter.  This application doesn't run under MapReduce, so I don't worry about Lucene timeouts.  Also, I have the entire collection preparsed, so I can easily shove those bits into HBase or any other system I want to.</body></html>
