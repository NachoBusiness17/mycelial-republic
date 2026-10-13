// Volumetric laser tracer tone-map fork (michael0884 lineage, operator-supplied)
// CHAIN ROLE: POST — reads the previous pass from iChannel0. XYZtosRGB supplied by fleet.
vec3 XYZtosRGB(vec3 c){
    return vec3(
        dot(c,vec3( 3.2406,-1.5372,-0.4986)),
        dot(c,vec3(-0.9689, 1.8758, 0.0415)),
        dot(c,vec3( 0.0557,-0.2040, 1.0570)));
}
vec3 ColorGrade(vec3 vColor){
    vec3 vHue=vec3(1.0,.7,.2);
    vec3 vGamma=1.0+vHue*0.6;
    vec3 vGain=vec3(.9)+vHue*vHue*8.0;
    vColor*=1.5;
    float fMaxLum=100.0;
    vColor/=fMaxLum;
    vColor=pow(vColor,vGamma);
    vColor*=vGain;
    vColor*=fMaxLum;
    return pow(tanh(vColor),vec3(0.57));
}
vec3 tone(vec3 c){c=XYZtosRGB(c);return ColorGrade(c);}
void mainImage(out vec4 fragColor,in vec2 fragCoord){
    vec4 acc=texture(iChannel0,fragCoord/iResolution.xy);
    fragColor=vec4(tone(0.03*acc.xyz/acc.w),1.0);
}
