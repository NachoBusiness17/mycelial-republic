// CALABI-YAU SOURCE CUSTODY — 2026-09-04
// Source: @YoheiNishitsuji (TU Delft GLSL artist). Hand-carried by operator 2026-09-04.
// License: all-rights-resumed assumed — techniques-credit basis: study and re-express,
// never redistribute rendered copies as own work. Credit @YoheiNishitsuji on any surface.
// Arc: shadow-fields layer 9 (watch/SHADERTOY_SHADOW_FIELDS_20260903.md) — projection of
// a hidden dimension: Calabi-Yau quintic z1^5+z2^5=1, 25 patches via complex-power
// parametrization, animated alpha rotates the projection plane inside 4D.
#define N 5
#define G 20
#define K 311.0
const float PI=3.14159265;
mat2 rot(float a){float c=cos(a),s=sin(a);return mat2(c,s,-s,c);}
vec2 cmul(vec2 a,vec2 b){return vec2(a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x);}
vec2 cpow(vec2 z,float e){float t=atan(z.y,z.x)*e;return pow(length(z),e)*vec2(cos(t),sin(t));}
void mainImage(out vec4 O,in vec2 F){
    vec2 uv=(F-iResolution.xy*0.5)/iResolution.y*1.2;
    float T=iTime,yaw=T*0.25,pit=0.55+0.3*sin(T*0.25);
    if(iMouse.z>0.0){ yaw=(iMouse.x/iResolution.x-0.5)*6.2832; pit=(iMouse.y/iResolution.y-0.5)*3.0; }
    float al=PI*0.25+0.4*sin(T*0.5), ca=cos(al), sa=sin(al);
    mat2 Ry=rot(yaw), Rp=rot(pit);
    vec2 P[N];  vec3 TT[N*N];
    for(int i=0;i<N;i++){ float p=6.2831853*float(i)/float(N); P[i]=vec2(cos(p),sin(p)); }
    for(int i=0;i<N*N;i++){ float f=float(i);
        TT[i]=0.5+0.5*cos(vec3(0,2.1,4.2)+floor(f/float(N))*1.26-mod(f,float(N))*1.26);}
    vec3 col=vec3(0);
    for(int m=0;m<G;m++)
    for(int n=0;n<G;n++){
        float a=(float(m)+0.5)/float(G)*PI*0.5;
        float b=((float(n)+0.5)/float(G)-0.5)*2.0;
        float ch=cosh(b), sh=sinh(b), c=cos(a), s=sin(a);
        vec2 w1=cpow(vec2(c*ch,-s*sh),0.4);
        vec2 w2=cpow(vec2(s*ch, c*sh),0.4);
        for(int k1=0;k1<N;k1++)
        for(int k2=0;k2<N;k2++){
            vec2 z1=cmul(w1,P[k1]), z2=cmul(w2,P[k2]);
            vec3 q=vec3(z1.x, z2.x, z1.y*ca+z2.y*sa);
            q.xz*=Ry; q.yz*=Rp;
            float w=q.z+4.5;
            vec2 dv=uv-q.xy/w;
            float d2=dot(dv,dv)*w*w*K;
            if(d2<16.0) col+=mix(vec3(1.0,0.85,0.55),vec3(0.3,0.45,0.9),clamp(length(q)*0.7,0.,1.))*exp(-d2-w*0.6);
        }
    }
    O=vec4(tanh(col*col),1.0);
}
