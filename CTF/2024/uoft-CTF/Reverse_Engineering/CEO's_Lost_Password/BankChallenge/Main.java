import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Base64;
import java.util.Map;
import java.util.Scanner;

public class Main {
    private static int a;

    private static long[] b = new long[13];

    static {
        b[0] = 2125394059L;
        b[1] = 316324253L;
        b[2] = 322717996L;
        b[3] = 1817181343L;
        b[4] = 1916880576L;
        b[5] = 1376134909L;
        b[6] = 1536615367L;
        b[7] = 969122838L;
        b[8] = 935365158L;
        b[9] = 2029694981L;
        b[10] = 538501427L;
        b[11] = 1099949760L;
        b[12] = 977807481L;
        a = (int) b[12] ^ 0x44E6D8F3;
    }

    static String passwordEncryptor(String password) {
        byte[] passByte = password.getBytes(StandardCharsets.UTF_8);
        int i = 1;
        while (i <= password.length()) {
            int j = 0;
            while (j < passByte.length) {
                int temp = (passByte[j] + (i - 12) * j + 6);
                passByte[j] = (byte) temp;
                j++;
            }
            i++;
        }
        return new String(Base64.getEncoder().encode(passByte), StandardCharsets.UTF_16);
    }

    static String passwordDecryptor(String password) {
        byte[] passByte = password.getBytes(StandardCharsets.UTF_16);
        passByte = Arrays.copyOfRange(passByte, 2, passByte.length - 1);
        System.out.println(new String(passByte, StandardCharsets.UTF_8));
        passByte = Base64.getDecoder().decode(passByte);
        int i = 1;
        while (i <= password.length()) {
            int j = 0;
            while (j < passByte.length) {
                int temp = (passByte[j] - (i - 12) * j - 6);
                passByte[j] = (byte) temp;
                j++;
            }
            i++;
        }
        return new String(passByte, StandardCharsets.UTF_8);
    }

    private static int mainPrograms() {
        String username;
        Scanner scanner = new Scanner(System.in);
        Map<String, a> map = Map.of("user", new a(convertString("ꙅꌕנּ뱜鰀"), 10.0F), "admin",
                new a(convertString("렒蘐鱇騢鼡謴꼾︻ꁏ꤅뤃ꔍ먅ꈽ"), 100000.0F));
        while (true) {
            System.out.println("Please enter your username:");
            username = scanner.nextLine();
            if (!map.containsKey(username)) {
                System.out.println("User not found");
                continue;
            }
            break;
        }
        while (true) {
            System.out.println("Please enter your password:");
            String password = scanner.nextLine();
            if (!((a) map.get(username)).checkPassword(password)) {
                System.out.println("Incorrect password!");
                continue;
            }
            System.out
                    .println("Welcome back " + username + "! your balance is " + ((a) map.get(username)).getBalance());
            scanner.close();
            return ((int) b[1] ^ 0x12DAB99D);
        }
    }

    public static String convertString(String paramString) {
        StringBuilder stringBuilder = new StringBuilder();
        int i = 0;
        while (i < paramString.length()) {
            char c = paramString.charAt(i);
            stringBuilder.append((char) (c ^ (int) b[10] ^ 0x20182D44));
            i++;
        }
        return stringBuilder.toString();
    }

    public static void main(String[] paramArrayOfString) {
        // System.out.println("==============================");
        // System.out.println("Welcome to TotallySecureBank");
        // System.out.println("==============================");
        // System.out.println();
        // System.exit(mainPrograms());
        System.out.println(passwordDecryptor(convertString("렒蘐鱇騢鼡謴꼾︻ꁏ꤅뤃ꔍ먅ꈽ")));
    }
}

/* Location:              D:\Programming\CySec\Cyber Security\CTF\202\\uoft-CTF\Reverse_Engineering\CEO's_Lost_Password\BankChallenge.jar!\Main.class
 * Java compiler version: 11 (55.0)
 * JD-Core Version:       1.1.3
 */