 ordens.forEach(order => {
  const tr = document.createElement('tr');
  const trContent = `
    <td>${order.NomeProduto}</td>
    <td>${order.NumeroProduto}</td>
    <td>${order.FormaPagamento}</td>
    <td class="${
      order.Estado === 'Declined'?
       'danger'  : order.Estado === 'Pending'  ? 'warning'
       : 'primary'  }">${order.Estado}</td>
    <td class="primary">Detalhes</td>
  `;

  tr.innerHTML = trContent;
  document.querySelector('table tbody').appendChild(tr);
});



