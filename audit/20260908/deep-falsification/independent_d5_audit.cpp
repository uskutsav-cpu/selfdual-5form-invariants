#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <vector>
using W=std::array<int,5>;
using Z=__int128_t;

W dom(W w){
    int neg=0; bool zero=false;
    for(int &x:w){ if(x<0) neg^=1; x=std::abs(x); if(x==0) zero=true; }
    std::sort(w.begin(),w.end(),std::greater<int>());
    if(!zero && neg) w[4] = -w[4];
    return w;
}
long long fact(int n){long long x=1;for(int i=2;i<=n;i++)x*=i;return x;}
long long osize(W w){
    for(int &x:w)x=std::abs(x);
    int z=std::count(w.begin(),w.end(),0);
    std::map<int,int> c;for(int x:w)c[x]++;
    long long den=1;for(auto [x,n]:c)den*=fact(n);
    return fact(5)*(1LL<<(z?5-z:4))/den;
}
Z choose(int n,int k){Z x=1;for(int i=1;i<=k;i++){x*=n-k+i;assert(x%i==0);x/=i;}return x;}
std::string s128(Z x){if(x==0)return"0";bool neg=x<0;if(neg)x=-x;std::string s;while(x){s.push_back('0'+x%10);x/=10;}if(neg)s.push_back('-');std::reverse(s.begin(),s.end());return s;}

int main(){
    // weights of the 126-dimensional chiral half of Lambda^5 C^10
    std::vector<std::pair<W,int>> wt;
    for(int a=-1;a<=1;a++)for(int b=-1;b<=1;b++)for(int c=-1;c<=1;c++)for(int d=-1;d<=1;d++)for(int e=-1;e<=1;e++){
        W w={a,b,c,d,e}; int supp=(a!=0)+(b!=0)+(c!=0)+(d!=0)+(e!=0); int pr=1;for(int x:w)if(x)pr*=x;
        if(supp==1)wt.push_back({w,3});
        else if(supp==3)wt.push_back({w,1});
        else if(supp==5 && pr==1)wt.push_back({w,1});
    }
    int total=0;for(auto [w,m]:wt)total+=m;assert(total==126);

    // Weyl denominator product prod_{alpha>0}(1-e^{-alpha}) on full exponent lattice
    std::map<W,long long> poly; poly[{0,0,0,0,0}]=1;
    for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)for(int sg: {-1,1}){
        W r={0,0,0,0,0};r[i]=1;r[j]=sg;
        auto next=poly;
        for(auto const& [w,c0]:poly){W q=w;for(int t=0;t<5;t++)q[t]-=r[t];next[q]-=c0;}
        for(auto it=next.begin();it!=next.end();){if(it->second==0)it=next.erase(it);else ++it;}
        poly.swap(next);
    }
    assert(poly.size()==1920);
    std::map<W,long long> den;
    for(auto const& kv:poly){W w=kv.first; auto c=kv.second; for(int &x:w)x=-x; den[dom(w)]+=c;}
    for(auto it=den.begin();it!=den.end();){if(it->second==0)it=den.erase(it);else ++it;}

    std::vector<std::map<W,Z>> ch(23);
    ch[0][{0,0,0,0,0}]=1;
    for(int n=0;n<=22;n++){
        if(n){
            auto &cur=ch[n];
            for(int A=0;A<=n;A++)for(int B=0;B<=A;B++)for(int C=0;C<=B;C++)for(int D=0;D<=C;D++)for(int E=-D;E<=D;E++){
                W lam={A,B,C,D,E};
                if((A+B+C+D+E-n)&1) continue;
                Z sum=0;
                for(int k=1;k<=n;k++){
                    int m=n-k;
                    for(auto [nu,mul]:wt){
                        W q; bool ok=true;
                        for(int i=0;i<5;i++){q[i]=lam[i]-k*nu[i];if(std::abs(q[i])>m){ok=false;break;}}
                        if(!ok)continue;
                        auto it=ch[m].find(dom(q)); if(it!=ch[m].end())sum += Z(mul)*it->second;
                    }
                }
                assert(sum>=0 && sum%n==0);
                if(sum)cur[lam]=sum/n;
            }
        }
        Z dim=0;for(auto [w,m]:ch[n])dim += m*osize(w);
        if(dim!=choose(125+n,n)){std::cerr<<"dimension mismatch "<<n<<"\n";return 3;}
        Z inv=0;for(auto [w,c]:den){auto it=ch[n].find(w);if(it!=ch[n].end())inv+=Z(c)*it->second;}
        std::cout<<n<<" "<<s128(inv)<<" "<<ch[n].size()<<"\n";
    }
}
