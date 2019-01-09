package engine;

import java.util.Arrays;
import java.util.List;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

import dev.*;
import dev.RealDevice.DeviceConfig;
/**
 * This is the main class which drives the application. Usage of this program
 * is as below:
 * <pre>
 * java engine.Main -c [Target count] -t [Max no. of worker threads] 
 * 		-q [How many workers tasks can be queued] 
 *      -d [Device type. real|unreal]
 *      -p [Print progress. Optional, defaults to false]
 *      -w [Max time in seconds to wait for this whole thing to complete. Optional, defaults to 900 sec.]
 *      -u [Compute delay in ms. Optional, defaults to 3.]
 *      -b [Device boot delay in ms. Optional, defaults to 250.]
 * Example:
 *      -c 50000 -t 20 -q 100 -d real -p -w 300
 * </pre>
 * You can specify two system properties to print more fine grained information:
 * <pre>
 * -DprintDevice will print the creation of thread local devices.
 * -DprintVariants will print the generation of variants by different tasks.
 * </pre>
 * @author Balwinder Sodhi
 */
public class Main {

	/**
	 * Flag that controls whether to use real device or unreal one.
	 */
	private static boolean USE_REAL_DEVICE = false;
	/**
	 * Target count of numbers that we want to generate.
	 */
	private int targetCount;
	/**
	 * How many workers tasks can be queued. This will dictate the size of 
	 * work queue.
	 */
	private int workQueueSize;
	/**
	 * How many concurrent threads can we have in order to process the 
	 * queued tasks.
	 */
	private int threadCount;
	/**
	 * A thread pool based executor.
	 */
	private ThreadPoolExecutor exec;
	/**
	 * The custom class which holds generated numbers to be tracked.
	 */
	private NumbersTracker numberTracker;
	/**
	 * Tracks the execution time of the program.
	 */
	private long timeTakenMs;
	/**
	 * Sets a timeout in seconds for the termination of all worker threads.
	 */
	private long maxWaitTimeInSec;
	/**
	 * Parsed command line args.
	 */
	private static CLIArgs cliArgs;

	/**
	 * In this constructor we initialize member fields including the custom 
	 * list as well as the thread pool executor.
	 */
	public Main() {
		USE_REAL_DEVICE = cliArgs.useRealDevice;
		this.targetCount = cliArgs.targetCount;
		this.workQueueSize = cliArgs.taskQueueSize;
		this.threadCount = cliArgs.threads;
		this.maxWaitTimeInSec = cliArgs.maxWaitTimeInSec;
		/**
		 * This is the main guy who manages allocation of tasks off the
		 * tasks queue to various threads. 
		 */
		this.exec = new ThreadPoolExecutor(
				/* Thread pool size */
				threadCount,
				/* Max thread pool size */
				threadCount,
				/* How long an idle thread will be kept alive */
				10, TimeUnit.SECONDS, 
				/*
				 * A blocking queue which holds computation task requests.
				 * Each thread in the pool will pick tasks off this queue
				 * as and when they become available.
				 */
				new LinkedBlockingQueue<Runnable>(workQueueSize),
				/*
				 * A policy specifying how we handle rejected tasks. A task
				 * can be rejected by ThreadPoolExecutor if the tasks queue
				 * is full and all threads are busy handling earlier tasks.
				 * The policy we use is a "back pressure" one which turns the
				 * calling (main) thread into a worker thread.
				 */
				new ThreadPoolExecutor.CallerRunsPolicy());
		
		this.numberTracker = new NumbersTracker(
				/* Starting variant */
				2,
				/* Target count. We reduce by 1 to adjust for 0 based indexing */
				this.targetCount-1,
				/* Print the progress of threads */
				cliArgs.printProgress);
	}

	/**
	 * Depending on the initial flag setting, this method creates a real
	 * or unreal (i.e. with zero latencies etc.) device.
	 * @return The device instance.
	 */
	public static Device makeDevice() {
		if (USE_REAL_DEVICE) {
			DeviceConfig config = new DeviceConfig(cliArgs.computeDelayInMs,
					cliArgs.bootDelayInMs, 2323 /* Seed for random num. */);
			return new RealDevice(config);
		} else {
			return new UnrealDevice(2341);
		}
	}

	/**
	 * Returns the execution time of the program in appropriate units.
	 * @param timeInMs Time in milli seconds.
	 * @return Time in appropriate units.
	 */
	private String getTimeTaken(long timeInMs) {
		StringBuilder sb = new StringBuilder();
		if (timeInMs < 1000) { // Less than 1 sec
			sb.append(timeInMs).append(" ms");
		} else if (timeInMs < 300000) { // Less than 5 min
			sb.append((float) timeInMs / 1000).append(" sec");
		} else {
			sb.append((float) timeInMs / 60000).append(" min");
		}
		return sb.toString();
	}

	/**
	 * This method drives the whole show. In a while loop, we continue to
	 * submit new tasks into the task queue until on of the {@link ComputationTask}
	 * issues a shutdown call to the thread pool executor.
	 */
	public void work() {
		long startTime = System.currentTimeMillis();
		try {
			System.out.println("Started the executor.");
			/**
			 * We continue submitting the computation tasks to TPE until it is
			 * signaled to be shutdown by one of the tasks on meeting the
			 * terminating condition.
			 */
			while (!exec.isShutdown()) {
				
				/*
				 * This puts a task into the TPE's queue. When the queue is 
				 * full and all worker threads are busy, then this main thread
				 * itself will start running the submitted task (due to 
				 * "back pressure" rejection policy), and hence slows down the
				 * generation of new tasks by this loop. 
				 */
				exec.submit(new ComputationTask(numberTracker, exec));
			}
			/**
			 * Set a timeout for the termination of all worker threads, 
			 * after the Executor is asked to shutdown.
			 */
			exec.awaitTermination(maxWaitTimeInSec, TimeUnit.SECONDS);
			timeTakenMs = System.currentTimeMillis() - startTime;

			// Print the results summary
			StringBuilder sb = new StringBuilder();
			sb.append("\n----------------------------------------");
			sb.append("\nRESULTS SUMMARY");
			sb.append("\n----------------------------------------");
			sb.append("\nTarget count................: " + targetCount);
			sb.append("\nNumber of threads...........: " + threadCount + " + main");
			sb.append("\nWork queue size.............: " + workQueueSize);
			sb.append("\nUsed real device............: " + USE_REAL_DEVICE);
			sb.append("\nTime taken..................: ").append(
					getTimeTaken(timeTakenMs));
			sb.append("\nResulting number............: ").append(
					numberTracker.getResultingTargetNumber());
			sb.append("\nTotal computations (approx).: ").append(
					exec.getCompletedTaskCount()* Device.MULTIPLIERS.length);
			System.out.println(sb);
			
		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}

	/**
	 * Driver method that runs this program. Usage is as below:
	 * <pre>
	 * java engine.Main -c [Target count] -t [Max no. of worker threads] 
	 * 		-q [How many workers tasks can be queued] 
	 *      -d [Device type. real|unreal]
	 *      -p [Print progress. Optional, defaults to false]
	 *      -w [Max time in seconds to wait for this whole thing to complete. Optional, defaults to 900 sec.]
	 *      -u [Compute delay in ms. Optional, defaults to 3.]
	 *      -b [Device boot delay in ms. Optional, defaults to 250.]
	 * Example:
	 *      -c 50000 -t 20 -q 100 -d real -p -w 300
	 * </pre>     
	 * @param args
	 */
	public static void main(String[] args) {
		
		try {
			processCLIArgs(args);			
			if (cliArgs.targetCount < 1 || cliArgs.threads < 1 || cliArgs.taskQueueSize < 1) {
				System.out.println("\nRequired arguments are missing.");
				String cn = Main.class.getName();
				System.out.println("Usage: java "+cn+ " [OPTIONS]\nOPTIONS include:"+
						"\n-c <Target count>\n-t <Max no. of worker threads>"+
						"\n-q <How many workers tasks can be queued> " +
						"\n-d <Device to use [real|unreal]. Optional, defaults to real> " +
						"\n-p <Print progress. Optional, defaults to false> " +
						"\n-w <Max time in seconds to wait for this whole thing to " +
						"complete. Optional, defaults to 900 sec.>" +
						"\n-u [Compute delay in ms. Optional, defaults to 3.]" +
						"\n-b [Device boot delay in ms. Optional, defaults to 250.]" +
						"\n\nYou can " +
						"specify two system properties to print more fine " +
						"grained information:\n-DprintDevice will print the " +
						"creation of thread local devices.\n-DprintVariants " +
						"will print the generation of variants by different tasks." +
						"\n\nExample:\n"+
						"java -DprintVariants "+cn+" -c 50000 -t 20 -q 100 -d real -p -w 300\n");
				return;
			}
		} catch (Exception e) {
			System.err.println("Could not parse input arguments!");
			e.printStackTrace();
			return;
		}
		Main m = new Main();
		m.work();
	}

	/**
	 * Process the CLI arguments supplied to run this program.
	 * @param args CLI arguments received.
	 * @return Object that represents the input arguments.
	 */
	private static void processCLIArgs(String[] args) {
		cliArgs = new CLIArgs();
		List<String> list = Arrays.asList(args);
		if (list.contains("-c")) cliArgs.targetCount = Integer.parseInt(list.get(list.indexOf("-c") + 1));
		if (list.contains("-t")) cliArgs.threads = Integer.parseInt(list.get(list.indexOf("-t") + 1));
		if (list.contains("-q")) cliArgs.taskQueueSize = Integer.parseInt(list.get(list.indexOf("-q") + 1));
		if (list.contains("-d")) cliArgs.useRealDevice = "real".equalsIgnoreCase(list.get(list.indexOf("-d") + 1));
		if (list.contains("-p")) cliArgs.printProgress = true;
		if (list.contains("-w")) cliArgs.maxWaitTimeInSec = Long.parseLong(list.get(list.indexOf("-w") + 1));
		if (list.contains("-u")) cliArgs.computeDelayInMs = Long.parseLong(list.get(list.indexOf("-u") + 1));
		if (list.contains("-b")) cliArgs.bootDelayInMs = Long.parseLong(list.get(list.indexOf("-b") + 1));
	}
	/**
	 * A wrapper for holding parsed CLI arguments.
	 */
	private static class CLIArgs {
		int targetCount;
		int threads;
		int taskQueueSize;
		boolean useRealDevice = true;
		boolean printProgress = false;
		long maxWaitTimeInSec = 900;
		long computeDelayInMs = 3;
		long bootDelayInMs = 250;
	}
}
