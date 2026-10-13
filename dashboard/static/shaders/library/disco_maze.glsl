// Disco Maze — by Noztol (shadertoy lineage; CC BY-NC-SA default)
// Wolfenstein-style DDA raycaster through a disco maze — hex floors, color walls.
// CHAIN ROLE: SCENE — auto-races, no input needed. PORTED VERBATIM minus iChannel use.
#define PI 3.1415926535
float hash1(float n){return fract(sin(n)*437518.56453)+.1;}
vec3 hsb2rgb(in vec3 c){
    vec3 rgb=clamp(abs(mod(c.x*6.+vec3(0.,4.,2.),6.)-3.)-1.,0.,1.);
    rgb=rgb*rgb*(3.-2.*rgb);
    return c.z*mix(vec3(1.),rgb,c.y);
}
float fbm(in vec2 st,float t){
    float value=(sin(t*5.*hash1(st.x+hash1(st.y)))+4.)*.25;
    return max(.75,pow(value,3.));
}
vec3 squaresColors(vec2 p,float t){
    float i=p.x;float j=p.y;
    return hsb2rgb(vec3(hash1(j+hash1(i)),.7,fbm(vec2(i,j),t)));
}
vec3 getDiscoSquares(vec2 p,float border,float t){
    vec2 ip=floor(p);vec2 fp=fract(p);
    ip.x=mod(ip.x,16.);
    vec3 tileColor=squaresColors(ip,t);
    float glow=1.-length(fp-.5)*1.2;
    glow=clamp(glow,.4,1.);
    tileColor*=glow;
    float edgeDist=max(abs(fp.x-.5),abs(fp.y-.5));
    float borderMask=smoothstep(border-.03,border,edgeDist);
    return mix(tileColor,vec3(.01),borderMask);
}
vec3 discoColors(vec2 p,float t){
    p+=vec2(t*.2);
    vec3 orange=vec3(1.,.4,.1)*2.;
    vec3 purple=vec3(1.,.2,.5)*.8;
    float l=pow(.5+.5*cos(p.x*PI*2.+cos(p.y)*8.)*sin(p.y*2.),4.)*2.;
    vec3 c=pow(l*(mix(orange,purple,.5+.5*cos(p.x*PI*12.+sin(p.y*10.)*3.))+mix(orange,purple,.5+.5*cos(p.x*PI*6.+sin(p.y*3.)*3.))),vec3(1.2))*.7;
    c+=vec3(1.,.8,.4)*pow(.5+.5*cos(p.x*PI*6.)*sin(p.y*12.),20.)*2.;
    c+=vec3(.1,.5+.5*cos(p*PI*6.))*vec3(.05,.1,.4).bgr*.7;
    return c;
}
vec4 hexCoords(vec2 uv){
    vec2 r=vec2(1.,1.7320508);
    vec2 h=r*.5;
    vec2 a=mod(uv,r)-h;
    vec2 b=mod(uv-h,r)-h;
    vec2 gv=dot(a,a)<dot(b,b)?a:b;
    vec2 id=uv-gv;
    return vec4(gv.x,gv.y,id.x,id.y);
}
vec3 getDiscoHexes(vec2 p,float border,float t){
    vec4 hc=hexCoords(p);
    vec2 gv=hc.xy;vec2 id=hc.zw*.125;
    float d=max(abs(gv.x),dot(abs(gv),vec2(.5,.8660254)));
    float m=1.-smoothstep(border-.03,border,d);
    m+=1.-smoothstep(0.,.22,length(gv));
    vec3 hexCol=m*discoColors(id,t);
    vec3 bgCol=vec3(.03,.01,.05);
    return bgCol+hexCol;
}
float mapM(vec2 p){
    vec2 id=floor(p);float L=6.;
    float corridorX=abs(id.y-floor(id.x/L)*L);
    float corridorY=abs(id.x-floor(id.y/L+1.)*L);
    if(corridorX<=1.||corridorY<=1.)return 0.;
    float n=fract(sin(dot(id,vec2(12.9898,78.233)))*43758.5453);
    return n>.3?1.:0.;
}
void mainImage(out vec4 fragColor,in vec2 fragCoord){
    float globTime=iTime+1.;
    float L=6.;float t=iTime*2.5;
    float seg=floor(t/L);float local_t=fract(t/L)*L;
    vec2 ro;
    if(mod(seg,2.)<.5){ro.x=floor(seg/2.)*L+local_t;ro.y=floor(seg/2.)*L;}
    else{ro.x=floor(seg/2.+.5)*L;ro.y=floor(seg/2.)*L+local_t;}
    float turnProgress=smoothstep(L-2.,L,local_t);
    float currentAngle=mod(seg,2.)<.5?0.:1.5707963;
    float nextAngle=mod(seg,2.)<.5?1.5707963:0.;
    float camAngle=mix(currentAngle,nextAngle,turnProgress);
    float bankRoll=sin(globTime*.6)*.15;
    mat2 rotM=mat2(cos(bankRoll),-sin(bankRoll),sin(bankRoll),cos(bankRoll));
    vec2 screenUV=rotM*((fragCoord*2.-iResolution.xy)/iResolution.y);
    vec2 camDir=vec2(cos(camAngle),sin(camAngle));
    vec2 camPlane=vec2(-camDir.y,camDir.x)*.8;
    vec2 rd=camDir+camPlane*screenUV.x;
    vec2 mapPos=floor(ro);
    vec2 deltaDist=abs(1./rd);
    vec2 stepDir=sign(rd);
    vec2 sideDist=(stepDir*(mapPos-ro)+(stepDir*.5)+.5)*deltaDist;
    float side=0.;float cellId=0.;
    for(int i=0;i<64;i++){
        if(sideDist.x<sideDist.y){sideDist.x+=deltaDist.x;mapPos.x+=stepDir.x;side=0.;}
        else{sideDist.y+=deltaDist.y;mapPos.y+=stepDir.y;side=1.;}
        cellId=mapM(mapPos);
        if(cellId>0.)break;
    }
    vec3 finalCol=vec3(0.);vec3 voidFog=vec3(.01,.002,.03);
    float perpWallDist=(side==0.)?(mapPos.x-ro.x+(1.-stepDir.x)*.5)/rd.x:(mapPos.y-ro.y+(1.-stepDir.y)*.5)/rd.y;
    float projectedHeight=1./perpWallDist;
    if(abs(screenUV.y)<projectedHeight&&cellId>0.){
        float wallX=(side==0.)?ro.y+perpWallDist*rd.y:ro.x+perpWallDist*rd.x;
        vec2 wallUV=vec2(wallX,screenUV.y/projectedHeight)*4.;
        finalCol=getDiscoSquares(wallUV,.46,globTime);
        if(side==1.)finalCol*=.6;
        finalCol=mix(finalCol,voidFog,smoothstep(2.,16.,perpWallDist));
    }else{
        float floorDist=1./abs(screenUV.y);
        vec2 floorPos=ro+rd*floorDist;floorPos*=2.5;
        finalCol=getDiscoHexes(floorPos,.46,globTime);
        finalCol=mix(finalCol,voidFog,smoothstep(2.,16.,floorDist));
    }
    finalCol*=1.2;
    fragColor=vec4(finalCol,1.);
}
