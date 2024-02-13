# Challenge Kepepet

**Category** : Web
**Points** : 968

Maybe this code will help you exploiting the challenge

app: http://ctf.ukmpcc.org:8080/

bot: http://ctf.ukmpcc.org:8081/

```
fn note_logic(mut note: FormNote) -> Response {
    let mut res = Response::new(200);
    if note.value.len() > 26 {
        res.set_status(302);
        utils::RQ::redirect(&mut res, "/note");
        return Ok(res);
    }
    let safe = ammonia::Builder::new()
        .add_generic_attribute_prefixes(&["hx-"])
        .rm_tags(&["script"])
        .clean(&note.value)
        .to_string();
    note.value = safe;
    if note.path.is_empty() {
        note.path = Uuid::new_v4().to_string();
    }
    let id = db::append(db::Note {
        id: note.path,
        value: note.value,
    })
    .expect("Something Wrong");
    utils::RQ::redirect(&mut res, format!("/note/{}", id));
    Ok(res)
}
```

Challenge bot configuration:
```env
    environment:
      APPNAME: Admin
      APPURL: http://app:8080/
      APPURLREGEX: ^.*$
      APPFLAG: fake{flag}
      APPLIMIT: 2
      APPLIMITTIME: 60
```
Bot source code: https://github.com/dimasma0305/CTF-XSS-BOT



