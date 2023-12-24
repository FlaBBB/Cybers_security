# Note Again

**Category** : Web
**Points** : 699

Oh, not(e) again....

- https://note-again.ctf.cyberjawara.id/
- https://bot.note-again.ctf.cyberjawara.id/

**Hint:**

I dunno why, but ChatGPT gave me this code.

```python
def RequestParser(model: typing.Type[BaseModel]):
    async def parse_request(request: Request) -> BaseModel:
        if request.headers.get('Content-Type') == 'application/json':
            data = await request.json()
        elif request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
            form_data = await request.form()
            data = dict(form_data)
        else:
            raise HTTPException(status_code=400, detail="Unsupported content type")
        
        return model(**data)
    return parse_request
		```

## Files : 
 - [bot.js](./bot.js)


