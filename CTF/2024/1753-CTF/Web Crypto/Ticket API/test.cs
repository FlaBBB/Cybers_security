using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

// Guid obj = Guid.NewGuid();
// Console.WriteLine("New Guid is " + obj.ToString());
// validate the guid
if (Guid.TryParse("b169be46-6891-4d39-ab38-4413545bccf7", out var result))
{
    Console.WriteLine("Valid Guid");
}
else
{
    Console.WriteLine("Invalid Guid");
}