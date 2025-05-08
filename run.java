package org.run;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.*;


public class run {


    public static boolean checkCapacity(int maxCapacity, List<Map<String, String>> guests) {
        List<Object[]> events = new ArrayList<>();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");

        for (Map<String, String> guest : guests) {
            try {
                if (!guest.containsKey("check-in") || !guest.containsKey("check-out")) {
                    throw new IllegalArgumentException("Missing 'check-in' or 'check-out' field");
                }
                LocalDate checkIn = LocalDate.parse(guest.get("check-in").trim(), formatter);
                LocalDate checkOut = LocalDate.parse(guest.get("check-out").trim(), formatter);
                events.add(new Object[]{checkIn, true});
                events.add(new Object[]{checkOut, false});
            } catch (Exception e) {
                return false;
            }

        }

        // Сортировка: по дате, выезд (false) раньше заезда (true)
        events.sort((a, b) -> {
            LocalDate dateA = (LocalDate) a[0];
            LocalDate dateB = (LocalDate) b[0];
            int cmp = dateA.compareTo(dateB);
            if (cmp != 0) return cmp;
            boolean isCheckInA = (Boolean) a[1];
            boolean isCheckInB = (Boolean) b[1];
            return Boolean.compare(isCheckInA, isCheckInB);
        });

        int current = 0;
        for (Object[] event : events) {
            boolean isCheckIn = (Boolean) event[1];
            if (isCheckIn) {
                current++;
                if (current > maxCapacity) return false;
            } else {
                current--;
            }
        }

        return true;
    }


    // Вспомогательный метод для парсинга JSON строки в Map
    private static Map<String, String> parseJsonToMap(String json) {
        Map<String, String> map = new HashMap<>();
        // Удаляем фигурные скобки
        json = json.substring(1, json.length() - 1);


        // Разбиваем на пары ключ-значение
        String[] pairs = json.split(",");
        for (String pair : pairs) {
            String[] keyValue = pair.split(":", 2);
            String key = keyValue[0].trim().replace("\"", "");
            String value = keyValue[1].trim().replace("\"", "");
            map.put(key, value);
        }

        return map;
    }


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);


        // Первая строка - вместимость гостиницы
        int maxCapacity = Integer.parseInt(scanner.nextLine());


        // Вторая строка - количество записей о гостях
        int n = Integer.parseInt(scanner.nextLine());


        List<Map<String, String>> guests = new ArrayList<>();


        // Читаем n строк, json-данные о посещении
        for (int i = 0; i < n; i++) {
            String jsonGuest = scanner.nextLine();
            // Простой парсер JSON строки в Map
            Map<String, String> guest = parseJsonToMap(jsonGuest);
            guests.add(guest);
        }


        // Вызов функции
        boolean result = checkCapacity(maxCapacity, guests);


        // Вывод результата
        System.out.println(result ? "True" : "False");


        scanner.close();
    }
}