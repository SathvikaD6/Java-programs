package sathvika;

public class Computer {
	class processor{
		public void displayDetails() {
			System.out.println("brand : Hp");
			System.out.println("speed : 150rpm");
		}
	}
	public static void main(String[] args) {
		Computer myObj1 = new Computer();
		Computer.processor myObj = myObj1.new processor();
		myObj.displayDetails();	
	}
}
