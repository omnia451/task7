#include <bits/stdc++.h>
using namespace std;


int main()
{
    int r,c,i,j,justiceLeagueScore = 0,villainsScore = 0;
    cin >> r >> c;

    int justiceLeague[r][c];
    int villains[r][c];

    for(i=0; i<r; i++)
    {
        for(j=0; j<c; j++)
        {
            cin.ignore();
            cin >> justiceLeague[i][j];
        }
    }

    for(i=0; i<r; i++)
    {
        for(j=0; j<c; j++)
        {
            cin.ignore();
            cin >> villains[i][j];
        }
    }

    for(i=0; i<r; i++)
    {
        for(j=0; j<c; j++)
        {
            if(justiceLeague[i][j] > villains[i][j])
            {
                justiceLeagueScore ++;
            }
            else if(justiceLeague[i][j] < villains[i][j])
            {
                villainsScore ++;
            }
        }
    }

    if(justiceLeagueScore > villainsScore)
    {
        cout << "Justice League";
    }
    else if(justiceLeagueScore < villainsScore)
    {
        cout << "Villains";
    }
    else
    {
        cout << "Tie";
    }

    return 0;
}
