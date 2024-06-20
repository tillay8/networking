import java.io.*;
import java.util.*;
//create file, edit it, delete it
public class test {
    public static void main(String[] args) {
        try {
            File file = new File("amongus.txt");
            if (file.createNewFile()) {
                System.out.println("File made :D");
            } else {
                System.out.println("duplicate error :(");
            }
            
            System.out.println("files in dir");
            File currentDir = new File(".");
            File[] files = currentDir.listFiles();
            for (File f : files) {
                System.out.println(f.getName());
            }
            
            FileWriter writer = new FileWriter(file, true); 
            writer.write("ruqeg9dshxvz\n");
            writer.close();
            System.out.println("text added :D");
            
            System.out.println("file contents");
            BufferedReader reader = new BufferedReader(new FileReader(file));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
            reader.close();
            
            if (file.delete()) {
                System.out.println("Deleted file :D");
            } else {
                System.out.println("delete error :(.");
            }
            
            System.out.println("Files in dir:");
            files = currentDir.listFiles();
            for (File f : files) {
                System.out.println(f.getName());
            }
            
        } catch (IOException e) {
            System.out.println("weird error :(");
            e.printStackTrace();
        }
    }
}

