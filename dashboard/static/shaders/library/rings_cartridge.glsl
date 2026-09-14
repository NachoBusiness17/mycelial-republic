// THE RINGS — fleet original — one ring per day since 2026-08-25.
// Lineage: operator's smoke-ring shader (shadertoy M3XBz4 iteration). CHAIN ROLE: SCENE.
// uDays = fleet day count (injected by the runner).
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
void mainImage(out vec4 fragColor,in vec2 fragCoord){
    vec2 uv=(fragCoord-.5*iResolution.xy)/iResolution.y;
    vec3 col=vec3(0.);
    float tt=.05*iTime;
    float pxAng=atan(uv.y,uv.x);
    float pxRad=length(uv);
    float ringRad=.35;
    float smokeFactor=1.7;
    float dA=abs(mod(pxAng-(6.28318*tt)+3.14159,6.28318)-3.14159);
    float totalRingEnv=1.-smoothstep(0.,smokeFactor,dA);
    for(int ii=0;ii<32;ii++){
        float i=float(ii);
        if(i>=uDays)break;
        float ringSpread=.01+.06*(i/10.);
        float freq=2.+mod(i,5.);
        float mainWave=ringSpread*sin((6.28318*tt+pxAng)*freq+i*1.7);
        float secWave=sin(pxRad*70.+(6.28318*tt+pxAng)*2.+i);
        vec2 cFlow=vec2(cos(6.28318*tt+pxAng),sin(6.28318*tt+pxAng));
        vec2 cTime=vec2(cos(6.28318*tt),sin(6.28318*tt));
        vec2 noiseInp=(2.+i*.2)*cFlow+.5*cTime+vec2(i*4.3,i*9.1);
        float turb=noise2(noiseInp);
        mainWave=totalRingEnv*mainWave;
        secWave=totalRingEnv*.015*secWave;
        turb=totalRingEnv*.03*turb;
        float dist=abs(pxRad-(ringRad+mainWave+secWave+turb));
        float radialD=abs(pxRad-ringRad);
        float radialFallOff=exp(-radialD*9.);
        col+=exp(-dist*dist*1e4)*.14*radialFallOff;
    }
    fragColor=vec4(col,1.);
}
