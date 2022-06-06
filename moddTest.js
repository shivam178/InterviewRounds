const arr = ['OR', ['<', 'a', 'b'], ['AND', ['==', 'c', 'd'], ['!=', 'e', 'f']]];
const resNeeded = 'a < b OR (c == d AND e != f)';
const operators = {
  'OR': 'or',
  'AND': 'and',
  '<': 'lessThan',
  '>': 'greaterThan',
  '==': 'equal',
  '!=': 'notEqual',
} //add any other operators which may be missing here

const getRes = (array) => {
  let res = '';
  if (Array.isArray(array[0])) {
    res += getRes([...array[0]]);
  } else if (operators[array[0]]) {
    const middleElement = array[0];
    const firstElement = getRes([...array[1]]);
    const secondElement = getRes([...array[2]]);
    res += `(${firstElement} ${middleElement} ${secondElement})`;
  } else {
    return array[0];
  }
  return res;
};

const res = getRes(arr);
console.log('res', res);
