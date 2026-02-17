import json
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

def get_main_window(app) -> HwndWrapper:
    p1 = find_element_by_auto_id("59648", app)
    p2 = find_element_by_auto_id("59664", p1)
    p2.SetFocus()
    return HwndWrapper(p2.CurrentNativeWindowHandle)

def tab_into_next_field(w: HwndWrapper):
    w.set_focus()
    w.type_keys("{TAB}")
    time.sleep(0.3)

def maybe_close_warning_dialog(app):
    dialog = find_element_by_auto_id("OverruleWarning", app)
    if dialog:
        el = HwndWrapper(dialog.CurrentNativeWindowHandle)
        el.close()
        time.sleep(0.5)

def get_input_value(value: str) -> str:
    return value.replace(" ", "{SPACE}")

def enter_data(entry: dict, tab_count: int = 50):
    app = find_element_by_class_name("CSIUTW2025")
    window = get_main_window(app)

    for i in range(tab_count):
        is_success = False
        is_error = False
        msg = f"{i}: "
        key = "<no-id>"
        try:
            element = uia.get_focused_element()
            el = HwndWrapper(element.CurrentNativeWindowHandle)
            key = str(el.element_info.control_id)    
            if key in entry:
                value = entry[key]["value"]
                el.type_keys(get_input_value(value))
                entry[key]["success"] = True
                is_success = True
            else:
                parent = el.parent()
                if parent is not None:
                    key = str(parent.element_info.control_id)
                    if key in entry:
                        value = entry[key]["value"]
                        parent.type_keys(get_input_value(value))
                        entry[key]["success"] = True
                        is_success = True    
            if len(entry) == 0:
                break
            tab_into_next_field(window)
        except Exception as e:
            msg += f"key: {key} error: {e}"
            is_error = True
            maybe_close_warning_dialog(app)
        finally:
            if not is_error:
                msg += f"key: {key} (success)" if is_success else f"key: {key} (no-match)"
            print(msg)

def main():
    ## Sandbox for testing
    data = {
        "20000": {"value": "S", "success": False},
        "20001": {"value": "123456789", "success": False},
        "20002": {"value": "ACME INC", "success": False},
        "20005": {"value": "1", "success": False},
        "20006": {"value": "S", "success": False},
        "20011": {"value": "X", "success": False},
        "20012": {"value": "X", "success": False},
        "20013": {"value": "X", "success": False},
        "20014": {"value": "2", "success": False},
        "20017": {"value": "X", "success": False},
        "20018": {"value": "123ABC", "success": False},
        "20019": {"value": "99956452", "success": False},
        "20020": {"value": "99956453", "success": False},
        "20021": {"value": "99956454", "success": False},
        "20022": {"value": "99956455", "success": False},
        "20023": {"value": "123 Main St.", "success": False},
        "20024": {"value": "Houston", "success": False},
        "20025": {"value": "TX", "success": False},
        "20026": {"value": "77002", "success": False},
        "20027": {"value": "375000", "success": False},
        "20028": {"value": "55000", "success": False},
        "20029": {"value": "75000", "success": False},
        "20030": {"value": "64000", "success": False},
        "20031": {"value": "100000", "success": False},
        "20033": {"value": "579", "success": False},
        "20034": {"value": "11000", "success": False},
        "20035": {"value": "12000", "success": False},
        "20036": {"value": "13000", "success": False},
        "20037": {"value": "67 Long-Bridge Ave.", "success": False},
        "20038": {"value": "New York", "success": False},
        "20039": {"value": "NY", "success": False},
        "20040": {"value": "10007", "success": False},
        "20044": {"value": "14000", "success": False},
        "20045": {"value": "15000", "success": False},
        "20046": {"value": "X", "success": False},
        "20047": {"value": "X", "success": False},
        "20048": {"value": "X", "success": False},
        "20049": {"value": "1231", "success": False},
        "20050": {"value": "104", "success": False},
        "20052": {"value": "TX", "success": False},
        "20055": {"value": "15000", "success": False},
        "20056": {"value": "16000", "success": False},
        "20057": {"value": "17000", "success": False},
        "20058": {"value": "AS", "success": False},
        "20059": {"value": "19000", "success": False}
    }
    enter_data(data, 100)
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()