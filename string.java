package Programs;
public class string {
	public static void main(String[] args) {
		String string = "This is Sathvika";
		int count = 0;
		int i;
		for(i = 0; i < string.length(); i++)
		{
			if(string.charAt(i) != ' ')
				count++;
        }
		System.out.println("The no.of characters in the string are: " + count);
	}
}
