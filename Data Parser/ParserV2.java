import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.Arrays;

public class ParserV2 {
    static Map<String, Integer> mapped = new HashMap<>();
    static String[] initializeSys(){
        Boolean first = true;
        String line = "";
        String csvFileMain = "start_station_probs.csv";
        String[] orgSet = new String[81];
        int i = 0;
        try (BufferedReader br = new BufferedReader(new FileReader(csvFileMain))) {
            while ((line = br.readLine()) != null) {
                if (first) {
                    first = false;
                }
                else {
                    String[] data = line.split(",");
                    String value = data[0];
                    orgSet[i] = value;
                    i++;
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return orgSet; 
    }
    static double[][] FindQ() {
        String[] indexSet = initializeSys();
        String csvFile = "trip_stats.csv";
        String line = "";
        String comma = ",";
        Boolean first = true;
        double[] total = new double[81];
        // Arrays.fill(total, 0.0);
        double[][] q = new double[81][82];   //Need this part
        // System.out.println("R"+q[1].length);
        //System.out.println(Arrays.toString(q));
        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {
            // int i = 0;
            while ((line = br.readLine()) != null) {
                if (first) {
                    first = false;
                }
                else {
                    String[] data = line.split(",");
                    int sourceIndex = Arrays.asList(indexSet).indexOf(data[0]);
                    int destinationIndex = Arrays.asList(indexSet).indexOf(data[1]);
                    int inputVal = Integer.parseInt(data[2]);
                    if (destinationIndex == -1) {
                        q[sourceIndex][81] += inputVal;
                    } else{
                        q[sourceIndex][destinationIndex] = inputVal;
                    }
                    // if (i<200) {System.out.println(inputVal);}
                    // i++;
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        for(int i = 0; i < q.length; i++){
            int tempTotal = 0;
            for(int j = 0; j < q[1].length; j++){
                tempTotal += q[i][j];
            }
            for(int j = 0; j < q[1].length; j++){
                q[i][j] = q[i][j]/tempTotal;
            }
        }
        return q;
    }
    public static void main(String[] args){
        double[][] x = FindQ();
        String output = "[";
        for(int i = 0; i < x.length; i++){
            String temp = "[";
            for(int j = 0; j < x[1].length; j++){
                if (j == 0){
                    temp += x[i][j];
                } else{
                    temp += ", " + x[i][j];
                }
            }
            if(i != x.length - 1){
                temp += "],";
            } else {
                temp += "]";
            }
            output += temp;
        }    
        output += "]";
        System.out.println(output);
    }
}
