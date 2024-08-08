package Programs;
class tree
{
	int x = 10;
	int y = 20;	
	void addition()
	{		
		System.out.println(x + y);
	}
}
class book
{
	int x = 40;
	int y = 30;
	void subtraction()
	{
		System.out.println(x - y);
	}
}
public class Main 
{
	int x = 5;
	int y = 6;
	public static void main(String[] args) 
	{
		Main myObj = new Main();
		Main myBox = new Main();
		System.out.println(myBox.x);
		System.out.println(myObj.y);
		tree x1 = new tree();
		x1.addition();
		book x2 = new book();
		x2.subtraction();
	}
}
