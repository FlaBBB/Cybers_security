// var flag = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}!@#$%^&*()_+|{}:<>?`-=[]\\;',./~";

// ==================================================================================================================
var seed = new DateTimeOffset(DateTime.Today.AddDays(0)).ToUnixTimeSeconds();
Console.WriteLine(seed);
// var random = new Random((int)seed);

// var randomBuffer = new byte[flag.Length];
// random.NextBytes(randomBuffer);

// var flagBuffer = Encoding.ASCII.GetBytes(flag);
// var resultBuffer = new byte[flag.Length];

// for (var i = 0; i < flag.Length; i++)
//     resultBuffer[i] = (byte)(randomBuffer[i] ^ flagBuffer[i]);

// var encrypted = string.Concat(resultBuffer.Select(x => x.ToString("X").PadLeft(2, '0')));

// Console.WriteLine(encrypted); // 22ECCDB90936D5C2454A65A5BB4C120FB1C8567381C6DB368EB57D4C6BE8B6D8C860E5C6FAC1F48BF2291A5C9EA3C354715857E7		  
