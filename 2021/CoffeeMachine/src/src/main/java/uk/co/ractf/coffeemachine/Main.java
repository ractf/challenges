package uk.co.ractf.coffeemachine;

import java.lang.reflect.InvocationTargetException;
import java.net.MalformedURLException;
import java.net.URL;

public class Main {

    public static void main(String[] args) throws IllegalAccessException, InvocationTargetException, InstantiationException, MalformedURLException, ClassNotFoundException {
        ClassLoader classLoader = new RejectingClassLoader(new URL[]{new URL(args[0])}, Main.class.getClassLoader());
        Class<?> clazz = classLoader.loadClass("Main");
        Runnable runnable = (Runnable) clazz.getConstructors()[0].newInstance();
        runnable.run();
    }

}
