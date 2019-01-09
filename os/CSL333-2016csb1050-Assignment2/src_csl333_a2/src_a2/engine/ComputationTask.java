package engine;

import java.util.concurrent.ExecutorService;

import dev.Device;

/**
 * This class implements the task which gets executed by concurrent threads.
 * 
 * @author Balwinder Sodhi
 */
public class ComputationTask implements Runnable {

	/**
	 * Custom data structure which is used to hold and track the generated
	 * numbers by various threads.
	 */
	private NumbersTracker numTracker;
	/**
	 * Instance of a device which generates the numbers according to specific
	 * formula.
	 */
	private static final ThreadLocal<Device> device = new ThreadLocal<Device>() {
		@Override
		protected Device initialValue() {
			if (System.getProperties().containsKey("printDevice")) {
				System.out.println(Utils.currentTime()
						+ ":: Created a thread local device for "
						+ Thread.currentThread().getName());
			}
			return Main.makeDevice();
		}
	};

	/**
	 * Reference to the task executor which runs these tasks.
	 */
	private ExecutorService executor;

	/**
	 * C'tor which initializes various fields.
	 * 
	 * @param numTracker
	 *            Custom data structure that holds and tracks generated nos.
	 * @param executor
	 *            Executor instance which runs these tasks.
	 */
	public ComputationTask(NumbersTracker numTracker, ExecutorService executor) {
		this.numTracker = numTracker;
		this.executor = executor;
	}

	/**
	 * This method contains the main logic for a concurrent task. We do the
	 * following here:
	 * 
	 * <pre>
	 * 1. Take the first element off the set of generated numbers
	 * 2. Start a loop which:
	 *    a) Runs as many times as we have variants in device
	 *    b) Invokes the device to calculate a number
	 *    c) If the generated number is bigger than current ceiling AND
	 *       set of generated numbers is empty, then shuts down the executor
	 *    d) Else, adds the generated number to the set.
	 * </pre>
	 */
	@Override
	public void run() {
		try {
			long base = 0, nxtNumber;
			try {
				base = numTracker.takeFirst();
				int endLoop = Device.MULTIPLIERS.length;
				for (int i = 0; i < endLoop; i++) {
					if (System.getProperties().containsKey("printVariants")) {
						System.out.println(Utils.currentTime() + ":: "
								+ Thread.currentThread().getName()
								+ " :: Generating " + i + "th variant...\n");
					}
					nxtNumber = device.get().f(base, i);
					if (numTracker.isDone(nxtNumber)) {
						executor.shutdown();
						break;
					}
					numTracker.addNumber(nxtNumber);
				}
			} catch (Exception e) {
				// Ignore
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
