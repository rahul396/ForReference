/**
 * Java program to determine type of Object at runtime in Java.
 * you can identify type of any object by three ways i..e by using instanceof,
 * getClass() and isInstance() method of java.lang.Class.
 * Java does have capability to find out type of object but its not called
 * as RTTI (Runtime type Identification) in C++.
 *
 * @author Javarevisited
 */

public class RuntimeTypeIdentificationTest {
 
 
    public static void main(String args[]) {
        //creating instance of sub class and storing into type of superclass
        Rule simpleRule = new BusinessRule();
     
        //determining type of object in Java using instanceof keyword
        System.out.println("Checking type of object in Java using instanceof ==>");
        if(simpleRule instanceof Rule){
            System.out.println("System rule is instance of Rule");
        }
        if(simpleRule instanceof SystemRule){
            System.out.println("System rule is instance of SystemRule");
        }
        if(simpleRule instanceof BusinessRule){
            System.out.println("System rule is instance of BusinessRule");
        }
     
        //determining type of object in Java using getClass() method
        System.out.println("Checking type of object in Java using  getClass() ==>");
        if(simpleRule.getClass() == Rule.class){
            System.out.println("System rule is instance of Rule");
        }
        if(simpleRule.getClass() == SystemRule.class){
            System.out.println("System rule is instance of SystemRule");
        }
        if(simpleRule.getClass() == BusinessRule.class){
            System.out.println("System rule is instance of BusinessRule");
        }
     
        //determining type of object in Java using isInstance() method
        //isInstance() is similar to instanceof operator and returns true even
        //if object belongs to sub class.
        System.out.println("Checking type of object in Java using  isInstance() ==>");
        if(Rule.class.isInstance(simpleRule)){
            System.out.println("SystemRule is instance of Rule");
        }
        if(SystemRule.class.isInstance(simpleRule)){
            System.out.println("SystemRule is instance of SystemRule");
        }
        if(BusinessRule.class.isInstance(simpleRule)){
            System.out.println("SystemRule is instance of BusinessRule");
        }
    }
 
}

class Rule{
    public void process(){
        System.out.println("process method of Rule");
    }
}

class SystemRule extends Rule{
 
    @Override
    public void process(){
        System.out.println("process method of SystemRule class");
    }
}

class BusinessRule extends Rule{
 
    @Override
    public void process(){
        System.out.println("process method of Business Rule class");
    }
}


