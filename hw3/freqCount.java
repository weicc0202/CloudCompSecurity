import java.io.IOException;
import java.util.StringTokenizer;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.lang.StringBuilder;
import java.lang.String;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class freqCount {
    public static class freqCountMapper extends Mapper<Object, Text, Text, IntWritable>{
        private final static IntWritable one  = new IntWritable(1);
        final static Pattern WORD_PATTERN = Pattern.compile("\\[([^\\]]+)\\]");

        private Text word = new Text();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            Matcher matcher = WORD_PATTERN.matcher(value.toString());
            while (matcher.find()) {
                String rowString = matcher.group();
                StringBuilder oclock = new StringBuilder(rowString);
                if(rowString.length()>=21){
                    oclock.setCharAt(16, '0');
                    oclock.setCharAt(17, '0');
                    oclock.setCharAt(19, '0');
                    oclock.setCharAt(20, '0');
                    word.set(oclock.toString());
                    context.write(word, one);
                }
                
            }
        }
    }

    public static class freqCountReducer extends Reducer<Text,IntWritable,Text,IntWritable> {
        private IntWritable result = new IntWritable();
        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int reduceSum = 0;
            for (IntWritable val : values) {
                reduceSum += val.get();
            }
            result.set(reduceSum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration config = new Configuration();
        Job job = Job.getInstance(config, "freqCount");
        job.setJarByClass(freqCount.class);
        job.setReducerClass(freqCountReducer.class);
        job.setMapperClass(freqCountMapper.class);
        job.setCombinerClass(freqCountReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

