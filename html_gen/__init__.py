from functools import partial
def _html_attr_joiner(attr, values):
    if values and len(values) != 0:
            if isinstance(values, str):
                result = values
            else:
                result =  " ".join(values)
            return f' {attr}="{result}"'
    else:
        return ''

def uctag(tag, classes=None,ids=None,attrs=None):
    return tag_decor(tag,closing=False,classes=classes,ids=ids,attrs=attrs)()()

def ctag(tag, text="", classes=None,ids=None,attrs=None):
    temp_gen = lambda: text
    return tag_decor(tag=tag,closing=True,classes=classes,ids=ids,attrs=attrs)(temp_gen)()


def tag_decor(tag, closing=True, classes=None, ids=None, attrs=None):
    def html_decor(func=None):
        def inner_func(*args, **kwargs):
            if func:
                res = func(*args, **kwargs)
            else:
                res = ""
            complete_tag = f"<{tag}" if closing else f"<{tag}"
            str_classes = _html_attr_joiner('class', classes)
            str_ids = _html_attr_joiner('id', ids)
            other = ""
            if attrs:
                for k , v in attrs.items():
                    other += _html_attr_joiner(k, v)
            if closing:
                complete_tag += f"{str_classes}{str_ids}{other}>{res}</{tag}>"
            else:
                complete_tag += f"{str_classes}{str_ids}{other}/>"

            return complete_tag
        return inner_func
    return html_decor

def tag_combiner(tags, parent=None):
    res = ""
    for tag in tags:
        if callable(tag):
            res += tag()
        else:
            res += tag

    if parent:
        return ctag(parent,res)
    return res

class Node(object):

    def __getattr__(self, name):
        try: 
            return self.__getattribute__(name)
        except AttributeError:
            return self[name]
    


    def __getitem__(self, key):
        return self.attrs.get(key, [])
    
    def __setitem__(self, key, value):
        if isinstance(value,str):
            self.attrs[key] = value
        else:
            self.attrs[key] = " ".join(value)

    def __str__(self):
        attrs = self.attrs.copy()
        classes = attrs.pop("class", [])
        ids = attrs.pop("ids", [])
        self._populate_innerHTML()
        #populate self.innerHTML
        if self.innerHTML != "":
            return ctag(self.tag, self.innerHTML, classes,ids, attrs) 
        else:
            return uctag(self.tag,classes,ids,attrs)


    def _populate_innerHTML(self):
        text = ""
        if len(self.innerElems) == 0:
            return self.innerHTML
        for elem in self.innerElems:
            elem._populate_innerHTML()
            if len(elem.innerElems) == 0:
                text += str(elem)
            else:
                elem._populate_innerHTML()
                text += str(elem)
        self.innerHTML = text
        return self.innerHTML


    def __init__(self, tag):
        self.tag = tag
        self.attrs = {}
        self.innerHTML = ""
        self.innerElems = []
        #TODO : INIT

    def at(self, key, value):
        self.attrs[key] = self.attrs.get(key, []) + [value]
        return self

    def class_(self, className=None):
        if not className:
            return self.attrs.get("class", [])
        else:
            if isinstance(className, str):
                self.at("class",className)
            else:
                self.attrs["class"] = list(className)
        return self
    
    def id_(self, idName):
        if not idName:
            return self.attrs.get("id", [])
        else:
            if isinstance(idName, str):
                self.at("id",idName)
            else:
                self.attrs["id"] = list(idName)
        return self

    def ae(self, el):
        self.innerElems.append(el)
        self.innerHTML = ""
        return self

    def text(self,set=None):
        if set:
            self.innerHTML = set
            self.innerElems = []
            return self
        else:
            return str(self)

    def __call__(self, el):
        return self.ae(el)

