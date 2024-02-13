import java.util.Random;

public class UzhWorld {
    public static final byte CELLS_X = 40;
    public static final byte CELLS_Y = 30;
    public static final int FRUIT_STEP_DELAY_SCALE = 1000;
    public static final int FRUIT_STEP_DELAY_K = 3000;
    private Random random;
    private UzhBody body;
    private Point fruit;
    private boolean fruitEaten = false;
    private int stepDelay = 400;
    private int eatenFruits = 0;

    public UzhWorld(long seed, byte initialDirection) {
        this.random = new Random(seed);
        Point initialPoint = new Point((byte) 20, (byte) 15);
        this.body = new UzhBody(initialPoint, initialDirection, (byte) 5);
        generateFruit();
    }

    public UzhBody getBody() {
        return this.body;
    }

    public Point getFruit() {
        return this.fruit;
    }

    public int getStepDelay() {
        return this.stepDelay;
    }

    public int getEatenFruits() {
        return this.eatenFruits;
    }

    public boolean advance(byte direction) {
        this.body.advanceHead(direction);
        if (this.fruitEaten) {
            this.fruitEaten = false;
        } else {
            this.body.shrinkTail();
        }

        Point headPoint = this.body.getHeadSegment().head;
        if (!this.body.headIntersects() && headPoint.x >= 0 && headPoint.y >= 0 && headPoint.x < 40 && headPoint.y < 30) {
            if (headPoint.equals(this.fruit)) {
                this.fruitEaten = true;
                generateFruit();
                this.stepDelay = this.stepDelay * 1000 / 3000;
                this.eatenFruits++;
            }
            return true;
        } else {
            return false;
        }
    }

    private void generateFruit() {
        do {
            this.fruit = new Point((byte) (Math.abs(this.random.nextInt()) % 40), (byte) (Math.abs(this.random.nextInt()) % 30));
        } while (this.body.pointIntersects(this.fruit));
    }
}
