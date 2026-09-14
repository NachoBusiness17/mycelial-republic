// THE TAVERN - fleet original, Sancho's first cartridge. CHAIN ROLE: SCENE.
// Five flames, one per ractor, arced around a hearth that burns the chain root.
// mengxi cinnabar / fen ink-blue / tesla arc-cyan / edison filament-amber / gopher ledger-green.
// The hearth pulse rides uBass, the room's life rides uEnergy. Each flame takes
// its turn to speak, round-robin, the way the room actually runs.
// Lineage: watch/tavern/room_2026-09-08.md (the Socratic night) and the desk that
// fired its replies. No stolen code - the fire is ours.

vec2 hash2(vec2 p){
    p=vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3)));
    return -1.+2.*fract(sin(p)*43758.5453123);
}
float noise2(in vec2 p){
    const float K1=.366025404;const float K2=.211324865;
    vec2 i=floor(p+(p.x+p.y)*K1);
    vec2 a=p-i+(i.x+i.y)*K2;
    float m=step(a.y,a.x);
    vec2 o=vec2(m,1.-m);
    vec2 b=a-o+K2;
    vec2 c=a-1.+2.*K2;
    vec3 h=max(.5-vec3(dot(a,a),dot(b,b),dot(c,c)),0.);
    vec3 n=h*h*h*h*vec3(dot(a,hash2(i+0.)),dot(b,hash2(i+o)),dot(c,hash2(i+1.)));
    return dot(n,vec3(70.));
}

vec3 flameCol(int i){
    if(i==0)return vec3(1.0,0.30,0.15);
    if(i==1)return vec3(0.35,0.55,1.0);
    if(i==2)return vec3(0.45,0.95,1.0);
    if(i==3)return vec3(1.0,0.72,0.28);
    return vec3(0.30,1.0,0.55);
}
vec2 flamePos(int i){
    if(i==0)return vec2(-0.42,-0.15);
    if(i==1)return vec2(-0.21,-0.235);
    if(i==2)return vec2(0.0,-0.265);
    if(i==3)return vec2(0.21,-0.235);
    return vec2(0.42,-0.15);
}
// the round-robin: each ractor takes a turn, swells while speaking
float speak(float i,float t){
    float turn=fract(t/14.0)*5.0;
    float d=abs(turn-i);d=min(d,5.0-d);
    return 1.0+0.85*(1.0-smoothstep(0.15,0.9,d));
}
// a candle flame: teardrop radius advected by rising noise
float flame(vec2 q,float h,float seed,float t){
    if(q.y<0.0||q.y>h)return 0.0;
    float rise=t*(2.2+0.4*seed)+seed*7.1;
    float wob=(noise2(vec2(q.y*9.0-rise,seed*3.3))-0.5);
    q.x-=wob*0.07*(q.y/h);
    float r=0.030*(1.0-0.85*q.y/h)*(0.6+0.4*exp(-3.0*q.y));
    float d=abs(q.x)/max(r,1e-4);
    float body=exp(-d*d*2.0);
    float tip=1.0-smoothstep(h*0.55,h,q.y);
    float root=smoothstep(0.0,0.012,q.y);
    return body*tip*root;
}

void mainImage(out vec4 fragColor,in vec2 fragCoord){
    vec2 uv=(fragCoord-0.5*iResolution.xy)/iResolution.y;
    float t=iTime;
    vec3 col=vec3(0.016,0.012,0.010);

    // the hearth: coals at the bottom center, burning the chain root
    vec2 hp=uv-vec2(0.0,-0.335);
    float flick=0.75+0.25*noise2(vec2(t*2.5,7.3));
    float hearth=exp(-dot(hp,hp)*60.0)*(1.2+2.5*uBass)*flick;
    col+=vec3(1.0,0.45,0.15)*hearth;
    float coal=exp(-abs(uv.y+0.37)*90.0)*exp(-uv.x*uv.x*18.0);
    col+=vec3(1.0,0.30,0.08)*coal*(0.8+0.6*flick+2.0*uBass);

    // five flames on the arc, each speaking in its turn
    for(int i=0;i<5;i++){
        vec2 pos=flamePos(i);
        vec2 q=uv-pos;
        float fi=float(i);
        float h=0.13*(1.0+0.12*sin(t*2.6+fi*2.4))*(0.8+0.5*uEnergy);
        float sp=speak(fi,t);
        vec3 fc=flameCol(i);
        float f=flame(q,h,fi,t)*sp;
        col+=fc*f*0.9;
        col+=fc*0.05*exp(-length(q)*7.0)*sp;
        // the table: each flame reflects in the wood
        if(uv.y<-0.30){
            vec2 qm=vec2(q.x,(-0.60-uv.y)-pos.y);
            col+=fc*flame(qm,h,fi,t)*0.14;
        }
    }

    // embers off the hearth, more when the music is alive
    for(int j=0;j<16;j++){
        float fj=float(j);
        vec2 hs=hash2(vec2(fj,3.7))*0.5+0.5;
        float sp=0.05+0.12*hs.y;
        float life=fract(t*sp*(0.5+hs.x)+hs.x);
        float wig=(noise2(vec2(life*6.0,fj*1.7))-0.5)*0.06;
        vec2 p=vec2((hs.x-0.5)*0.16+wig,-0.30+life*0.55);
        float b=(1.0-life)*(0.35+0.65*uEnergy);
        vec2 dp=uv-p;
        col+=vec3(1.0,0.6,0.25)*b*exp(-dot(dp,dp)*9000.0);
    }

    // room grain + the dark that makes fire worth watching
    col+=(noise2(uv*680.0+t)-0.5)*0.015;
    col*=exp(-dot(uv,uv)*1.1);
    fragColor=vec4(col,1.0);
}
