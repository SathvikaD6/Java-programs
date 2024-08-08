package Programs;
public class swap2 {
	public static void main(String[] args) {
		int x = 10;
		int y = 20;
		x = x + y;
		y = x - y;
		x = x - y;
		System.out.println("After swapping the value of x is: " + x);
		System.out.println("After swapping the value of y is: " + y);

	}

}
