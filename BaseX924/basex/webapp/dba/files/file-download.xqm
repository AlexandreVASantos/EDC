(:~
 : Download file.
 :
 : @author Christian Grün, BaseX Team 2005-19, BSD License
 :)
module namespace dba = 'dba/files';

import module namespace session = 'dba/session' at '../modules/session.xqm';

(:~
 : Downloads a file.
 : @param  $name  name of file
 : @return binary data
 :)
declare
  %rest:GET
  %rest:path("/dba/file/{$name}")
function dba:files(
  $name  as xs:string
) as item()+ {
  let $path := session:directory() || $name
  return (
    web:response-header(
      map { 'media-type': 'application/octet-stream' },
      map { 'Content-Length': file:size($path) }
    ),
    file:read-binary($path)
  )
};
