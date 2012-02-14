// This sets the output directory or module
namespace py MittoTest

typedef i16 Integer16

const Integer16 oneTwoThree = 123;

/* This is a test file */

/* This is a enum */
enum Numbers
{
  ONE = 1TWO
  THREE
  FIVE = 89;
  SIX,
  EIGHT
}

# A unix-style comment

enum Empty
{
}

struct Insanity
{
  1: map<Numbers, i64> userMap
}

/* enum Invisible
{
  BLEEP
  BLOOP
} */

// Bla bla bla bla

////// llololool

/* And this is a constant */
const Numbers myNumbers = Numbers.ONE,
const string myString = 'This // is a string';
const string myAnotherString = "This /* is */ a another string"
