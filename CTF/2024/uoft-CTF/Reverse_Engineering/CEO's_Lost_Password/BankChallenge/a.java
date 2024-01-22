class a {
    private final String password;
    private final float balance;

    a(String password, float balance) {
        this.password = password;
        this.balance = balance;
    }

    boolean checkPassword(String password) {
        return Main.passwordEncryptor(password).equals(this.password);
    }

    public float getBalance() {
        return this.balance;
    }
}

/* Location:              D:\Programming\CySec\Cyber Security\CTF\202\\uoft-CTF\Reverse_Engineering\CEO's_Lost_Password\BankChallenge.jar!\a.class
 * Java compiler version: 11 (55.0)
 * JD-Core Version:       1.1.3
 */