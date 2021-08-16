package uk.co.ractf.coffeemachine;

public class SecureStorage {

    public static String getFlag() {
        boolean authorized = false;
        for (final StackTraceElement stackTraceElement : new Throwable().getStackTrace()) {
            if (stackTraceElement.getClassName().startsWith("uk.co.ractf.coffeemachine") &&
                    !stackTraceElement.getClassName().equals("uk.co.ractf.coffeemachine.SecureStorage") &&
                    !stackTraceElement.getClassName().equals("uk.co.ractf.coffeemachine.Main")) {
                authorized = true;
            }
        }

        if (!authorized) {
            throw new IllegalArgumentException("Not authorized to read the flag!");
        }
        return "ractf{aaa}";
    }

}
