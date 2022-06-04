$(function() {
  $('.selectAllButton').on('click', function () {
    // すべてにチェックが入っている場合は解除する
    var targetDiv = $(this).parent().parent();
    var countAll = targetDiv.find('input.custom-checkbox').length;
    var countChecked = targetDiv.find('input.custom-checkbox:checked').length;
    if (countAll === countChecked) {
      targetDiv.find('input.custom-checkbox').prop('checked', false);
    } else {
      targetDiv.find('input.custom-checkbox').prop('checked', true);
    }
  });
})
