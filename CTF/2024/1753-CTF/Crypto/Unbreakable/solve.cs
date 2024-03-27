string encrypted = "22ECCDB90936D5C2454A65A5BB4C120FB1C8567381C6DB368EB57D4C6BE8B6D8C860E5C6FAC1F48BF2291A5C9EA3C354715857E7";

byte[] encryptedBytes = Enumerable.Range(0, encrypted.Length)
    .Where(x => x % 2 == 0)
    .Select(x => Convert.ToByte(encrypted.Substring(x, 2), 16))
    .ToArray();

var start_seed = new DateTimeOffset(DateTime.Today.AddDays(-345)).ToUnixTimeSeconds();
var end_seed = new DateTimeOffset(DateTime.Today.AddDays(0)).ToUnixTimeSeconds();
for (var seed = start_seed; seed < end_seed; seed++)
{
    var random = new Random((int)seed);

    var randomBuffer = new byte[encryptedBytes.Length];
    random.NextBytes(randomBuffer);

    var resultBuffer = new byte[encryptedBytes.Length];

    for (var i = 0; i < encryptedBytes.Length; i++)
        resultBuffer[i] = (byte)(randomBuffer[i] ^ encryptedBytes[i]);

    if (resultBuffer.All(x => x >= 32 && x <= 126))
    {
        var decrypted = Encoding.ASCII.GetString(resultBuffer);
        Console.WriteLine(decrypted);
    }
    // break;
}