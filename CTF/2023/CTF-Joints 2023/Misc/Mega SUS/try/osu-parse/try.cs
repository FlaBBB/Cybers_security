using OsuParsers.Beatmaps;
using OsuParsers.Decoders;

namespace SomeNamespace
{
    class Program
    {
        public static void Main(string[] args)
        {
            Beatmap beatmap = BeatmapDecoder.Decode(@"../flag.sus");
            
            //printing beatmap's title
            System.Console.WriteLine(beatmap.MetadataSection.TitleUnicode);
        }
    }
}