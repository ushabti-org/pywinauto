import time
from releases.pywinauto069.pywinauto.uia_defines import IUIA
from releases.pywinauto069.pywinauto.controls.hwndwrapper import HwndWrapper

uia = IUIA()
root = uia.root

def find_element_by_class_name(class_name, root=None):
    _root = root if root is not None else uia.root
    condition = uia.iuia.CreatePropertyCondition(
        uia.UIA_dll.UIA_ClassNamePropertyId,
        class_name
    )
    window = _root.FindFirst(uia.UIA_dll.TreeScope_Subtree, condition)
    return window

def find_element_by_auto_id(auto_id, root=None):
    _root = root if root is not None else uia.root
    condition = uia.iuia.CreatePropertyCondition(
        uia.UIA_dll.UIA_AutomationIdPropertyId,
        auto_id
    )
    window = _root.FindFirst(uia.UIA_dll.TreeScope_Subtree, condition)
    return window

def print_descendants(element):
    true_condition = uia.iuia.CreateTrueCondition()
    all_desc = element.FindAll(uia.UIA_dll.TreeScope_Descendants, true_condition)
    count = all_desc.Length
    for i in range(count):
        child = all_desc.GetElement(i)
        try:
            aid = child.CurrentAutomationId
            name = child.CurrentName
            ctrl = child.CurrentControlType
            clss = child.CurrentClassName

            print(f"AID={aid} | Name={name} | ControlType={ctrl} | ClassName={clss}")

        except Exception:
            pass

def get_main_window() -> HwndWrapper:
    window = find_element_by_class_name("CSIUTW2025")
    p1 = find_element_by_auto_id("59648", window)
    p2 = find_element_by_auto_id("59664", p1)
    p2.SetFocus()
    return HwndWrapper(p2.CurrentNativeWindowHandle)

def tab_into_next_field(w: HwndWrapper):
    w.set_focus()
    w.type_keys("{TAB}")
    time.sleep(0.3)


def enter_data(entry: dict, tab_count: int = 50):
    def on_successful_entry(key):
        del entry[key]
        print(f"successfully entered: {key}, remaining: {len(entry)}")
    
    window = get_main_window()

    for i in range(tab_count):
        try:
            element = uia.get_focused_element()
            el = HwndWrapper(element.CurrentNativeWindowHandle)
            key = str(el.element_info.control_id)
            if key in entry:
                value = entry[key]
                el.type_keys(value)
                on_successful_entry(key)
            else:
                parent = el.parent()
                if parent is not None:
                    key = str(parent.element_info.control_id)
                    if key in entry:
                        value = entry[key]
                        parent.type_keys(value)
                        on_successful_entry(key)
            if len(entry) == 0:
                print("all entries have been entered - stopping")
                break
            tab_into_next_field(window)

        except Exception as e:
            print(f"ran into an error for field: {key} value: {value} error: {e}")


def main():
    ## Sandbox for testing
    enter_data({
        "20000": "S",
        "20001": "123456789",
        "20002": "ACME INC",
        "20005": "1",
        "20006": "S",
        "20011": "X",
        "20012": "X",
        "20013": "X",
        "20014": "2",
        "20017": "X",
        "20018": "123ABC",
        "20019": "99956452",
        "20020": "99956453",
        "20021": "99956454",
        "20022": "99956455",
        "20023": "123 Main St.",
        "20024": "Houston",
        "20025": "TX",
        "20026": "77002",
        "20027": "375000",
        "20028": "55000",
        "20029": "75000",
        "20030": "64000",
        "20031": "100000",
        "20033": "579",
        "20034": "11000",
        "20035": "12000",
        "20036": "13000",
        "20037": "67 Long-Bridge Ave.",
        "20038": "New York",
        "20039": "NY",
        "20040": "10007",
        "20044": "14000",
        "20045": "15000",
        "20046": "X",
        "20047": "X",
        "20048": "X",
        "20049": "1231",
        "20050": "104",
        "20052": "TX",
        "20055": "15000",
        "20056": "16000",
        "20057": "17000",
        "20058": "AS",
        "20059": "19000"
    })

if __name__ == "__main__":
    main()