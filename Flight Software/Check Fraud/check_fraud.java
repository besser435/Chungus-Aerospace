import java.util.Scanner;

/* Check Fraud Launchpad Software
 *
 * https://github.com/besser435?tab=repositories
 */

public class check_fraud {
   public static void main(String[] args) {
      Scanner scnr = new Scanner(System.in);
      mainMenu();
      scnr.close();
   }





   static void mainMenu() {
      Scanner scnr = new Scanner(System.in);
      System.out.println("Check Fraud Launchpad Software");
      System.out.println("1. Begin Ignition Countdown");
      System.out.println("2. Ignite Now");
      System.out.print("Enter an option: ");
  

      int whichOption = scnr.nextInt();  
      if (whichOption == 1) {
         System.out.println("sent 1"); 
      }
      else if (whichOption == 2) {
         System.out.println("sent 2");  
      }
      else {
         System.out.println("Invalid Option");  
      }

      scnr.close();
   }
}
