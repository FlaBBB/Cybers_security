public class Point {
    public static final byte LEFT = -1;
    public static final byte RIGHT = 1;
    public static final byte UP = -2;
    public static final byte DOWN = 2;
    public byte x;
    public byte y;

    public Point(byte x, byte y) {
        this.x = x;
        this.y = y;
    }

    public Point(Point point) {
        this.x = point.x;
        this.y = point.y;
    }

    public void move(byte direction, byte distance) {
        switch (direction) {
            case UP:
                this.y += distance;
                break;
            case LEFT:
                this.x -= distance;
                break;
            case RIGHT:
                this.x += distance;
                break;
            case DOWN:
                this.y -= distance;
                break;
            default:
                throw new RuntimeException("Invalid direction");
        }
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Point)) {
            return false;
        }
        Point other = (Point) obj;
        return this.x == other.x && this.y == other.y;
    }

    @Override
    public String toString() {
        return "(" + this.x + ", " + this.y + ")";
    }

    public static String directionToString(byte direction) {
        switch (direction) {
            case UP:
                return "UP";
            case LEFT:
                return "LEFT";
            case RIGHT:
                return "RIGHT";
            case DOWN:
                return "DOWN";
            default:
                throw new RuntimeException("Invalid direction");
        }
    }

    public static byte invertDirection(byte direction) {
        return (byte) (-direction);
    }
}
