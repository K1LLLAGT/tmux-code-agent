export const areas=['Agent','Terminal','Files','Editor','Git','Activity','Settings'];
export function fileConflict(expected,current){return expected!==current?'stale':'clean';}
export function layout(width){return width>=900?'tablet':'phone';}
export function settingsValid(x){return ['READ_ONLY','SAFE','NORMAL','YOLO'].includes(x.profile)&&['OFF','LOCAL','APPROVAL','ENABLED'].includes(x.network);}
