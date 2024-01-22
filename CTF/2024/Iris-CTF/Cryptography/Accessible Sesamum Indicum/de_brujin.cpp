// C++ implementation of
// the above approach
#include <bits/stdc++.h>
using namespace std;

unordered_set<string> seen;
vector<int> edges;

// Modified DFS in which no edge
// is traversed twice
void dfs(string node, int &k, string &A)
{
    for (int i = 0; i < k; ++i)
    {
        string str = node + A[i];
        if (seen.find(str) == seen.end())
        {
            seen.insert(str);
            dfs(str.substr(1), k, A);
            edges.push_back(i);
        }
    }
}

// Function to find a de Bruijn sequence
// of order n on k characters
string deBruijn(int n, int k, string A)
{

    // Clearing global variables
    seen.clear();
    edges.clear();

    string startingNode = string(n - 1, A[0]);
    dfs(startingNode, k, A);

    string S;

    // Number of edges
    int l = pow(k, n);
    for (int i = 0; i < l; ++i)
        S += A[edges[i]];
    S += startingNode;

    return S;
}

// Driver code
int main()
{
    int n = 4, k = 17;
    string A = "0123456789abcdef";

    cout << deBruijn(n, k, A);

    return 0;
}