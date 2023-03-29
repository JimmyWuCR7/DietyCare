import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

class TryAPI {
    public static void main(String args[]) throws Exception {
        String baseUrl = "http://flask-env.eba-vyrxyu72.us-east-1.elasticbeanstalk.com";
        String path = "/dishIntakeList?";
        String params = "user_id=123&" + "intake_date=2022-01-14";
        put(baseUrl + path + params);
    }

    public static void put(String uri) throws Exception {
        URL url = new URL(uri) ;
        // Open a connection(?) on the URL(??) and cast the response(???)
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();

        // Now it's "open", we can set the request method, headers etc.
        connection.setRequestProperty("accept", "application/json");
        connection.setRequestMethod("GET");

        // This line makes the request
        InputStream responseStream = connection.getInputStream();
        BufferedInputStream bis = new BufferedInputStream(responseStream);
        ByteArrayOutputStream buf = new ByteArrayOutputStream();
        for (int result = bis.read(); result != -1; result = bis.read()) {
            buf.write((byte) result);
        }
        String response = buf.toString("UTF-8");

        System.out.println(response);

    }
}
