
// Source code is decompiled from a .class file using FernFlower decompiler.
import java.util.Scanner;

public class input_validator {
    private static final int FLAG_LEN = 34;

    public input_validator() {
    }

    private static boolean validate(String input_flag, String key) {
        int[] temp1 = new int[34];
        int[] cipher = new int[] { 1102, 1067, 1032, 1562, 1612, 1257, 1562, 1067, 1012, 902, 882, 1397, 1472, 1312, 1442,
                1582, 1067, 1263, 1363, 1413, 1379, 1311, 1187, 1285, 1217, 1313, 1297, 1431, 1137, 1273, 1161, 1339,
                1267, 1427 };

        int i;
        for (i = 0; i < 34; ++i) {
            temp1[i] = input_flag.charAt(i) ^ key.charAt(i);
        }

        for (i = 0; i < 34; ++i) {
            temp1[i] -= key.charAt(33 - i);
        }

        int[] temp2 = new int[34];

        for (i = 0; i < 17; ++i) {
            temp2[i] = temp1[1 + i * 2] * 5;
            temp2[i + 17] = temp1[i * 2] * 2;
        }

        for (i = 0; i < 34; ++i) {
            temp2[i] += 1337;
        }

        for (i = 0; i < 34; ++i) {
            if (temp2[i] != cipher[i]) {
                return false;
            }
        }

        return true;
    }

    public static void main(String[] var0) {
        Scanner sc = new Scanner(System.in);
        String key = "oF/M5BK_U<rqxCf8zWCPC(RK,/B'v3uARD";
        System.out.print("Enter input: ");
        String input_flag = sc.nextLine();
        if (input_flag.length() != 34) {
            System.out.println("Input length does not match!");
        } else {
            if (validate(new String(input_flag), key)) {
                System.out.println("Correct");
            } else {
                System.out.println("Wrong");
            }

        }
    }
}
