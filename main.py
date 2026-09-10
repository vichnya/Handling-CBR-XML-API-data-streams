import json
import pandas
import requests
from xml.etree import ElementTree as ET

class Component():
  def get_currencies(self, currencies_ids_lst: list) -> dict:
    pass

class ConcreteComponent(Component):  
  def __init__(self, lst):
    self._currencies_list = lst
    
  @property
  def get_currencies(self):
      cur_res_str = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
      result = []

      root = ET.fromstring(cur_res_str.content)
      valutes = root.findall("Valute")

      for _v in valutes:
          valute_id = _v.get('ID')
          valute = {}
          if (str(valute_id) in self._currencies_list):
              valute_cur_name, valute_cur_val = _v.find(
                  'Name').text, _v.find('Value').text
              valute_charcode = _v.find('CharCode').text
              valute[valute_charcode] = (valute_cur_name, valute_cur_val)
              result.append(valute)

      return result

  @get_currencies.setter
  def currencies_list(self, lst):
      self._currencies_list = lst


class Decorator(Component):  
    _component: Component = None

    def __init__(self, currencies_lst: Component):
        self._component = currencies_lst

    @property
    def wrapped_object(self) -> str:
        return self._component

    def get_currencies(self) -> dict:
        return self._component._currencies_list

class ConcreteDecoratorJSON(Decorator):
    def get_currencies(self) -> str:
        return f"ConcreteDecoratorJSON({json.dumps(self.wrapped_object.currencies_list, indent=4, ensure_ascii=False)})"


class ConcreteDecoratorCSV(Decorator):
    def get_currencies(self) -> str:
        res = json.dumps(self.wrapped_object.currencies_list, indent=4, ensure_ascii=False)
        return f"ConcreteDecoratorCSV({pandas.read_json(res).to_csv()})"


def show_currencies(currencies: ConcreteComponent):
    print(currencies.currencies_list)
  

if __name__ == '__main__':

  simple = ConcreteComponent(['R01090B', 'R01565', 'R01720'])
  print("Client: I've got a simple component:")
  show_currencies(simple)

  print()
  wrappedcurlist = Decorator(simple)
  wrappedcurlist_json = ConcreteDecoratorJSON(simple)
  print(wrappedcurlist_json.get_currencies())

  print()
  wrappedcurlist_csv = ConcreteDecoratorCSV(simple)
  print(wrappedcurlist_csv.get_currencies())