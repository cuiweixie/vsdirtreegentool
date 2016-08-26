import  xml.dom.minidom
import string
import sys

filterToBeAdd = {"other":1}
def fixItem(doc, fileItem):
	path = fileItem.getAttribute("Include")
	arr = path.split("\\")
	filterText = "default"
	for i in range(1, len(arr)):
		filterText = "\\".join(arr[0:i])
		filterToBeAdd[filterText] = 1
	arr2 = fileItem.getElementsByTagName("Filter")

	if len(arr2) > 0:
		arr2[0].firstChild.data = filterText
		filterToBeAdd[filterText] = 1
	else:
		filterEle = doc.createElement("Filter")
		nameT = doc.createTextNode(filterText)
		filterToBeAdd[filterText] = 1
		filterEle.appendChild(nameT)
		fileItem.appendChild(filterEle)
def proccess():
	doc = xml.dom.minidom.parse(sys.argv[1])
	changeTagName = ["ClCompile", "ClInclude", "None"]
	fileItems = []
	for name in changeTagName:
		fileItems.extend(doc.getElementsByTagName(name))
	for fileItem in fileItems:
		fixItem(doc, fileItem)
	filterGroup = doc.getElementsByTagName("ItemGroup")[0]
	for filterEle in filterGroup.getElementsByTagName("Filter"):
		filterGroup.removeChild(filterEle)
	id_str = "67DA6AB6-F800-4c08-8B7A-83BB121AA"
	start = 100
	for filterText in filterToBeAdd:
		filterEle = doc.createElement("Filter")
		filterEle.setAttribute("Include", filterText)
		uId = doc.createElement("UniqueIdentifier")
		textNode = doc.createTextNode("{" + id_str + str(start) + "}")
		start = start + 1
		uId.appendChild(textNode)
		filterEle.appendChild(uId)
		filterGroup.appendChild(filterEle)
	f= open(sys.argv[1], "w")
	print "file", f
	doc.writexml(f, addindent=' ', newl='\n')
if __name__ == "__main__":
	proccess()