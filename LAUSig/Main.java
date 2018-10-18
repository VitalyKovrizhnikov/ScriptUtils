import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.io.File;
import java.io.FileWriter;
import java.nio.file.Files;
import java.nio.file.FileSystems;
import java.nio.file.Paths;
import java.nio.file.Path;
import java.io.IOException;
import java.nio.charset.Charset;


public class Main {

private static final char[] hexArray = "0123456789ABCDEF".toCharArray();

public static String bytesToHex(byte[] bytes) {
    char[] hexChars = new char[bytes.length * 2];
    for ( int j = 0; j < bytes.length; j++ ) {
        int v = bytes[j] & 0xFF;
        hexChars[j * 2] = hexArray[v >>> 4];
        hexChars[j * 2 + 1] = hexArray[v & 0x0F];
    }
    return new String(hexChars);
}

    public static byte[] calcDigest(byte[] rawMessage, byte[] rawkey) throws InvalidKeyException {
        assert rawMessage != null;
        assert rawkey != null;
		byte[] bytes;
		try{
        Mac sha256_HMAC = Mac.getInstance("HmacSHA256");
		
        SecretKeySpec secret_key = new SecretKeySpec(rawkey, "HmacSHA256");
        sha256_HMAC.init(secret_key);
        bytes = sha256_HMAC.doFinal(rawMessage);
		return bytes;
		}catch(NoSuchAlgorithmException ex){
			System.out.println(ex);
		}
		return new byte[1];
    }
	


public static void main(String[] args){
	System.out.println("GO");
	String leftKey = args[0];
	System.out.println(args[0]);
	String rightKey = args[1];
	System.out.println(args[1]);
	System.out.println(args[2]);

	for (int i = 2; i < args.length; i++) {
		System.out.println(args[i]);
		try{
			byte[] msg = Files.readAllBytes(Paths.get(args[i]));
			Path outputFile = Paths.get(args[i] + ".sig");
			//System.out.println(new String(msg));
			//System.out.println(bytesToHex(calcDigest(msg, (leftKey + rightKey).getBytes(Charset.forName("US-ASCII")))));
			String output = new String(msg) 
							+ "{S:{MDG:" 
							+ bytesToHex(calcDigest(msg, (leftKey + rightKey).getBytes(Charset.forName("US-ASCII")))) 
							+ "}}";
			System.out.println(output);				
			Files.write(outputFile, output.getBytes(Charset.forName("US-ASCII")));				
		
        }catch(IOException ex){
            System.out.println(ex.getMessage());
        }catch (InvalidKeyException ex) {
			System.out.println(ex.getMessage());
	    }
		          
    }

 }	
}