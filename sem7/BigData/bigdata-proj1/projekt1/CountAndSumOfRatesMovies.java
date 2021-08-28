import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.log4j.Logger;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

public class CountAndSumOfRatesMovies extends Configured implements Tool {

    private static final Logger LOG = Logger.getLogger(CountAndSumOfRatesMovies.class);

    public static void main(String[] args) throws Exception {
        int res = ToolRunner.run(new CountAndSumOfRatesMovies(), args);
        System.exit(res);
    }

    public int run(String[] args) throws Exception {
        Job job = Job.getInstance(getConf(), "countAndSumOfRatesMovies");
        job.setJarByClass(this.getClass());
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        job.setMapperClass(Map.class);
        job.setCombinerClass(CountAndSumOfRatesMoviesReducer.class);
        job.setReducerClass(CountAndSumOfRatesMoviesReducer.class);
        job.setOutputKeyClass(LongWritable.class);
        job.setOutputValueClass(CountAndSumOfRates.class);
        return job.waitForCompletion(true) ? 0 : 1;
    }

    public static class Map extends Mapper<LongWritable, Text, LongWritable, CountAndSumOfRates> {

        private LongWritable movieId = new LongWritable();
        private CountAndSumOfRates countAndSumOfRates = new CountAndSumOfRates();

        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {
            try {
                if (key.get() == 0)
                    return;
                else {
                    String line = value.toString();
                    int i = 0;
                    for (String word : line.split(",")) {
                        if (i == 1) {
                            movieId.set(Integer.parseInt(word));
                        }
                        if (i == 3) {
                            countAndSumOfRates.set(
                                    new LongWritable(1),
                                    new LongWritable(Integer.parseInt(word))
                            );
                        }
                        i++;
                    }
                    context.write(movieId, countAndSumOfRates);
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public static class CountAndSumOfRatesMoviesReducer
            extends Reducer<LongWritable, CountAndSumOfRates, LongWritable, CountAndSumOfRates> {
        private CountAndSumOfRates result;

        @Override
        public void reduce(LongWritable key, Iterable<CountAndSumOfRates> values,
                           Context context) throws IOException, InterruptedException {
            this.result = new CountAndSumOfRates();
            for (CountAndSumOfRates countAndSumOfRates : values) {
                this.result.addCountAndSumOfRates(countAndSumOfRates);
            }
            context.write(key, result);
        }

    }

    public static class CountAndSumOfRates implements WritableComparable<CountAndSumOfRates> {

        private LongWritable count;
        private LongWritable sum;

        public CountAndSumOfRates() {
            set(new LongWritable(0), new LongWritable(0));
        }

        public void set(LongWritable count, LongWritable sum) {
            this.count = count;
            this.sum = sum;
        }

        public LongWritable getCount() {
            return count;
        }

        public LongWritable getSum() {
            return sum;
        }

        public void addCountAndSumOfRates(CountAndSumOfRates countAndSumOfRates) {
            set(new LongWritable(this.count.get() + countAndSumOfRates.getCount().get()),
                    new LongWritable(this.sum.get() + countAndSumOfRates.getSum().get()));
        }

        @Override
        public int compareTo(CountAndSumOfRates countAndSumOfRates) {
            int comparision = this.count.compareTo(countAndSumOfRates.getCount());
            if (comparision != 0) {
                return comparision;
            }
            return this.sum.compareTo(countAndSumOfRates.getSum());
        }

        @Override
        public void write(DataOutput dataOutput) throws IOException {
            this.count.write(dataOutput);
            this.sum.write(dataOutput);
        }

        @Override
        public void readFields(DataInput dataInput) throws IOException {
            this.count.readFields(dataInput);
            this.sum.readFields(dataInput);
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            CountAndSumOfRates countAndSumOfRates = (CountAndSumOfRates) obj;
            return this.count.equals(countAndSumOfRates.getCount()) && this.sum.equals(countAndSumOfRates.getSum());
        }

        @Override
        public int hashCode() {
            return this.count.hashCode() + this.sum.hashCode() * 31;
        }

        @Override
        public String toString() {
            return this.count.toString() + "\t" + this.sum.toString();
        }
    }
}

