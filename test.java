import java.io.*;
import java.util.*;

public class test {
    public static void main(String[] args) {
        try {
            // Create a new file named test.txt
            File file = new File("test.txt");
            if (file.createNewFile()) {
                System.out.println("File created: " + file.getName());
            } else {
                System.out.println("File already exists.");
            }
            
            // List files in the current directory
            System.out.println("Files in current directory:");
            File currentDir = new File(".");
            File[] files = currentDir.listFiles();
            for (File f : files) {
                System.out.println(f.getName());
            }
            
            // Add "ruqeg9dshxvz" to the contents of test.txt
            FileWriter writer = new FileWriter(file, true); // true for append mode
            writer.write("ruqeg9dshxvz\n");
            writer.close();
            System.out.println("Added 'ruqeg9dshxvz' to test.txt");
            
            // Show the contents of test.txt
            System.out.println("Contents of test.txt:");
            BufferedReader reader = new BufferedReader(new FileReader(file));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
            reader.close();
            
            // Delete test.txt
            if (file.delete()) {
                System.out.println("Deleted the file: " + file.getName());
            } else {
                System.out.println("Failed to delete the file.");
            }
            
            // List files in the directory after deletion
            System.out.println("Files in current directory after deletion:");
            files = currentDir.listFiles();
            for (File f : files) {
                System.out.println(f.getName());
            }
            
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }
}

