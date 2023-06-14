import subprocess

from tables.custom import Bookmark, IndexedHashTable, WikiIndex

from willmann import GenericMode

from plugin.utils import register
from plugin.widget import InputListStack 

class SearchMode(GenericMode):

    def __init__(self, port=None, parent_port=None, config=None):

        super(SearchMode, self).__init__(
                 port=port, 
                 parent_port=parent_port, 
                 config=config)

        self.mode=None

        self.wiki=WikiIndex()
        self.document=IndexedHashTable()
        self.bookmark=Bookmark()

        self.setUI()
        self.setMode('all')

    def setUI(self):

        self.ui=InputListStack()
        self.ui.main.input.setLabel('Index')
        self.ui.main.returnPressed.connect(self.confirm)

        self.ui.installEventFilter(self)

    def toggle(self): 

        if not self.ui.isVisible():
            self.activate()
        else:
            self.deactivate()

    def setMode(self, mode):

        self.mode=mode
        self.ui.main.input.setLabel(mode.title())
    
    @register('w')
    def setWikiMode(self):

        self.ui.show()
        self.setMode('wiki')

    @register('b')
    def setBookmarkMode(self):

        self.ui.show()
        self.setMode('bookmark')

    @register('d')
    def setDocumentMode(self):

        self.ui.show()
        self.setMode('document')

    @register('p')
    def setPartMode(self):

        self.ui.show()
        self.setMode('part')

    @register('a')
    def setAllMode(self):

        self.ui.show()
        self.setMode('all')

    def confirm(self):

        item=self.ui.main.list.currentItem()

        if item and 'id' in item.itemData:

            d=item.itemData
            kind=d['itemKind']
            print(d['hash'])
            if kind=='wiki':
                os_cmd=['kitty', '--class', 'floating', 'vim', d['path']]
                p=subprocess.Popen(os_cmd)
            elif kind=='document':
                os_cmd=['lura', d['path']]
                p=subprocess.Popen(os_cmd)
            elif kind=='url':
                os_cmd=['google-chrome-stable', d['url']]
                p=subprocess.Popen(os_cmd)

            self.ui.hide()

        else:

            self.find()

    @register('f')
    def find(self):

        self.ui.show()
        query=self.ui.main.input.text()

        dlist=[]
        if self.mode in ['wiki', 'all']:

            try:

                founds=self.wiki.search(query)
                for f in founds:
                    dlist+=[{'up':f['title'], 'id':f['path'], 'itemKind': 'wiki'}]

            except:

                pass


        if self.mode in ['bookmark', 'all']:

            try:

                blist=self.bookmark.search(query)
                for f in blist:
                    f['up']=f['title']
                    f['itemKind']=f['kind']
                    if f['kind']=='url':
                        f['down']=f['url']
                    elif f['path']:
                        f['down']=f['path']
                    else:
                        raise
                dlist+=blist

            except:
                pass

        if self.mode in ['document', 'part', 'all']:

            try:

                if self.mode=='document': query+=' AND kind:document'
                plist=self.document.search(query)
                for f in plist:
                    f['down']=f['path']
                    f['itemKind']='document'
                    if f['title']:
                        f['up']=f['title']
                    else:
                        f['up']=f['path']
                dlist+=plist

            except:
                pass

        if not dlist:
            dlist=[{'up': 'No match found', 'down': query}]

        self.ui.main.setList(dlist)

    @register('c') 
    def toggleCommands(self):

        self.ui.toggleCommands()

if __name__=='__main__':
    app=SearchMode(port=33333)
    app.toggle()
    app.run()
