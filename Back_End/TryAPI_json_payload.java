import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

class TryAPI {
    public static void main(String args[]) throws Exception {
        String baseUrl = "http://flask-env.eba-vyrxyu72.us-east-1.elasticbeanstalk.com";
        String path = "/dishIntakeList";
        String payload = "{\"user_id\": \"12334\", \"gender\": \"Male\", \"age\": \"14\", \"height\": \"12\", \"weight\": \"34\", \"target_weight\": \"12334\", \"body_fat\": \"12334\", \"body_type\": \"12334\", \"allergens\": \"\", \"diet_goal\": \"loseweight\", \"is_vegetarian\": \"True\"}";
        put(baseUrl + path, payload);
    }

    public static void put(String uri, String payload) throws Exception {
        HttpURLConnection connection = null;
        InputStream is = null;

        try {
            //Create connection
            URL url = new URL(uri);
            connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("PUT");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setRequestProperty("Content-Length", Integer.toString(payload.getBytes().length));
            connection.setRequestProperty("Content-Language", "en-US");  
            connection.setUseCaches(false);
            connection.setDoOutput(true);

            //Send request
            System.out.println(payload);
            DataOutputStream wr = new DataOutputStream (
            connection.getOutputStream());
            wr.writeBytes(payload);
            wr.close();

            //Get Response  

                is = connection.getInputStream();

            BufferedReader rd = new BufferedReader(new InputStreamReader(is));


            StringBuilder response = new StringBuilder(); // or StringBuffer if Java version 5+
            String line;
            while ((line = rd.readLine()) != null) {
                response.append(line);
                response.append('\r');
            }
            rd.close();
            System.out.println(response.toString());
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }
}
