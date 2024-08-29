package sathvika;

public class Dog {
	String Name,colour;
	public Dog(String x,String y) {
		Name = x;
		colour = y;
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Dog myObj = new Dog("candy", "black and white");
		System.out.println(myObj.Name);
		System.out.println(myObj.colour);
	}

}
