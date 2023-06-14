import os
import zmq
import subprocess

from willmann import GenericMode

from plugin.utils import register
from plugin.widget import InputListStack, InputList

class DocumentsMode(GenericMode):

    def __init__(self, port=None, parent_port=None, config=None):

        super(DocumentsMode, self).__init__(
                 port=port, 
                 parent_port=parent_port, 
                 config=config)


        self.mode=None
        self.current_dhash=None
        self.parts=DocumentParts()

        self.setUI()
        self.setData('documents')

    def setUI(self):

        self.ui=InputListStack()
        self.ui.hideWanted.connect(self.deactivate)

        self.ui.main.returnPressed.connect(self.confirm)
        self.ui.installEventFilter(self)

    def setConnection(self):

        super().setConnection()
        if self.parser_port:
            self.psocket=zmq.Context().socket(zmq.PUSH)
            self.psocket.connect(f'tcp://localhost:{self.parser_port}')

    def toggle(self): 

        if not self.ui.isVisible():
            self.activate()
        else:
            self.deactivate()

    def setMode(self, mode):

        self.mode=mode
        self.ui.main.input.setLabel(mode.title())
    
    @register('d')
    def showAllDocuments(self):

        self.ui.showMainWidget()
        self.setData('documents')

    @register('r')
    def showReference(self):

        self.ui.showMainWidget()
        if self.mode=='documents': self.setHash()
        self.setData('reference')

    @register('a')
    def showAbstract(self):

        self.ui.showMainWidget()
        if self.mode=='documents': self.setHash()
        self.setData('abstract')

    @register('o')
    def showOutline(self):

        self.ui.showMainWidget()
        if self.mode=='documents': self.setHash()
        self.setData('section')

    @register('k')
    def showKeyword(self):

        self.ui.showMainWidget()
        if self.mode=='documents': self.setHash()
        self.setData('keyword')

    @register('s')
    def showSummary(self):

        self.ui.showMainWidget()
        if self.mode=='documents': self.setHash()
        self.setData('summary')

    @register('p')
    def showParagraph(self):

        self.ui.showMainWidget()
        if self.mode=='documents': self.setHash()
        dlist=self.setData('paragraph')

    @register('b')
    def showBibliography(self):

        self.ui.showMainWidget()
        if self.mode=='documents': self.setHash()
        self.setData('bibliography')

    def getDocumentData(self, hash_data):

        hash_data['kind']='document'
        hash_data['down']=hash_data['path']
        meta=self.parts.metadata.getRow({'hash':hash_data['hash']})
        if meta and 'title' in meta:
            hash_data['up']=meta['title']
        return hash_data
        
    def setData(self, kind, dhash=None):

        if not dhash: 
            dhash=self.current_dhash
        # if not dhash:
            # return self.showAllDocuments()
        self.setMode(kind)
        dlist=[]
        if kind=='documents':
            data=self.parts.hash.getAll()
            for d in data:
                dlist+=[self.getDocumentData(d)]
        elif kind=='reference':
            cites=[]
            if dhash:
                data=self.parts.cite.getRow({'citing_hash':dhash})
                if data:
                    for d in data:
                        cites+=self.parts.metadata.getRow({'bibkey':d['cited_bibkey']})
            else:
                cites=self.parts.metadata.getAll()
            for d in cites:
                b=f'{d["author"]}, {d["year"]}'
                dlist+=[{'up':d['title'], 'down':b, 'kind':'cite'}]
        else:
            table=getattr(self.parts, kind, None)
            if table:
                if dhash:
                    data=table.getRow({'hash':dhash})
                else:
                    data=table.getAll()
                for d in data:
                    doc_data=self.parts.metadata.getRow({'hash':d['hash']})
                    if doc_data:
                        name=doc_data[0]['title']
                    else:
                        name=d['hash']
                    dlist+=[{'up':d['text'], 'down':name, id:d['hash'], 'kind':kind}]
        self.ui.main.setList(dlist)
        self.ui.show()
        return dlist

    @register('h')
    def setHash(self):

        item=self.ui.main.currentItem()
        if item: self.current_dhash=item.itemData.get('hash', None)

    @register('c') 
    def toggleCommands(self):

        self.ui.toggleCommands()

    def confirm(self):

        path=None
        page=0
        x, y = 0, 0
        if not self.current_dhash and self.mode=='documents':
            item=self.ui.main.currentItem()
            if item: self.current_dhash=item.itemData['hash']
        if self.current_dhash:
            r=self.parts.hash.getRow({'hash':self.current_dhash})
            for res in r:
                p=res['path']
                if os.path.isfile(p):
                    path=p
                    break

        if path:
            self.ui.hide()
            subprocess.Popen(['lura', '-p', str(page), '-x', str(x), '-y', str(y), path])

if __name__=='__main__':
    app=DocumentsMode(port=33333)
    app.show()
    app.run()
