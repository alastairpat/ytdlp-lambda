package xyz.omnigrove;

public class App 
{
    public static String helloWorld( String[] args )
    {
        return "hello, world";
    }

    public static void main(String[] args) {
        com.amazonaws.services.lambda.runtime.api.client.AWSLambda.main(args);
    }
}
