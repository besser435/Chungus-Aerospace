import java.util.Scanner;
import java.util.Date; 


/* Check Fraud Launchpad Software
 *
 * https://github.com/besser435?tab=repositories
 */

public class check_fraud {
   public static boolean debugMode = false;
   public static int launchCountdown = 10;

   public static void main(String[] args) {
      mainMenu();
   }

   
   static void relay(int state) {
      if (debugMode == false){   //this is so im not deafened while working on the thing
         if (state == 0) {
            //relay off;
         }
         if (state == 1) {
            //relay on;
         }
      }
   }


   static void beeper(int state) {
      if (debugMode == false){   //this is so im not deafened while working on the thing
         if (state == 0) {
            //beeper off;
         }
         if (state == 1) {
            //beeper on;
         }
      }
   }
   

   static void ignition() {
      System.out.println("Relay On");
      //Thread.sleep(1000);

   }


   static void delayCountdown() {
      Scanner scnr = new Scanner(System.in);
      System.out.println("Are you sure you want to start the countdown? y/n ");

      
      //String whichOption = scnr.nextLine();
      String whichOption = scnr.next();
      //scnr.close();
      if (whichOption.equals("y")) {
         System.out.println("Starting Countdown. Press CTRL + C to cancel");
         //Thread.sleep(1000);
         for (int i = launchCountdown; i > 0; i--) {
            System.out.println(i);
         }
         



      } else {
         System.out.println("Countdown Cancelled");
         mainMenu();
      }
      scnr.close(); 
   }


   static void mainMenu() {
      Scanner scnr = new Scanner(System.in);
      System.out.println("Check Fraud Launchpad Software");
      System.out.println("1. Begin Ignition Countdown");
      System.out.println("2. Ignite Now");
      System.out.print("Enter an option: ");

      int whichOption = scnr.nextInt(); 
      //int whichOption = scnr.next();
      //scnr.close();
      switch (whichOption) {
         case 1:
            delayCountdown();
            break;
         case 2:
            //ignite();
            break;
         default:
            System.out.println("Invalid option");
            mainMenu();
            break;
      }
      scnr.close();
   }
}
